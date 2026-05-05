#!/usr/bin/env python3
"""
05-assemble-video.py — ffmpeg-concat the chosen takes into final.mp4.

Walks runs/<run-dir>/shot-*/take-best.mp4 (symlinks chosen in step 6 of
the workflow), concatenates them in shot-id order with optional crossfades,
writes runs/<run-dir>/final.mp4.

Falls back to take-1.mp4 for any shot without a take-best.mp4 symlink.

Uses ffmpeg via subprocess — no extra Python deps.
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.session import emit_status, fail  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run-dir", type=Path, required=True)
    p.add_argument("--output", type=Path, default=None, help="Defaults to <run-dir>/final.mp4")
    p.add_argument("--crossfade-ms", type=int, default=0, help="0 = hard cuts; >0 = xfade duration")
    p.add_argument("--force", action="store_true", help="Overwrite final.mp4 if it exists")
    return p.parse_args()


def pick_take(shot_dir: Path) -> Path | None:
    best = shot_dir / "take-best.mp4"
    if best.exists():
        # Resolve in case it's a symlink to a take-N.mp4
        return best.resolve() if best.is_symlink() else best
    fallback = shot_dir / "take-1.mp4"
    if fallback.exists():
        emit_status("warn", message="no take-best.mp4, using take-1.mp4", shot=shot_dir.name)
        return fallback
    return None


def ffmpeg_check() -> None:
    if shutil.which("ffmpeg") is None:
        fail("FFMPEG_MISSING", "ffmpeg not on PATH. Install with: brew install ffmpeg")


def concat_hard_cut(takes: list[Path], output: Path) -> None:
    """Use ffmpeg's concat demuxer — fastest, no re-encode if codecs match."""
    list_file = output.parent / "_concat-list.txt"
    list_file.write_text(
        "\n".join(f"file '{t.as_posix()}'" for t in takes) + "\n",
        encoding="utf-8",
    )
    try:
        cmd = [
            "ffmpeg",
            "-y" if True else "-n",  # -y unconditional since we gated on --force
            "-f", "concat",
            "-safe", "0",
            "-i", str(list_file),
            "-c", "copy",
            str(output),
        ]
        emit_status("ffmpeg", cmd=" ".join(cmd))
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            # Codec mismatch is the most common failure here. Re-encode fallback.
            emit_status("ffmpeg_fallback", reason="concat failed, re-encoding", stderr=result.stderr[-500:])
            cmd_re = [
                "ffmpeg", "-y",
                "-f", "concat", "-safe", "0",
                "-i", str(list_file),
                "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-c:a", "aac", "-b:a", "128k",
                str(output),
            ]
            result = subprocess.run(cmd_re, capture_output=True, text=True)
            if result.returncode != 0:
                fail("FFMPEG_FAILED", result.stderr[-1000:])
    finally:
        list_file.unlink(missing_ok=True)


def concat_with_xfade(takes: list[Path], output: Path, xfade_ms: int) -> None:
    """
    Concat with crossfades using the xfade filter. Requires re-encoding.
    For each pair (i, i+1), offset = sum of preceding durations - xfade.
    """
    if len(takes) == 1:
        return concat_hard_cut(takes, output)

    # Probe each take's duration for offset arithmetic.
    durations = []
    for t in takes:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(t)],
            capture_output=True, text=True,
        )
        if out.returncode != 0:
            fail("FFPROBE_FAILED", out.stderr)
        durations.append(float(out.stdout.strip()))

    xfade_s = xfade_ms / 1000.0
    inputs = []
    for t in takes:
        inputs += ["-i", str(t)]

    # Build filter_complex chain. Naming: [vN], [aN] for video/audio of stream N.
    filter_parts = []
    last_v = "[0:v]"
    last_a = "[0:a]"
    cumulative = durations[0]
    for i in range(1, len(takes)):
        offset = cumulative - xfade_s
        filter_parts.append(
            f"{last_v}[{i}:v]xfade=transition=fade:duration={xfade_s}:offset={offset}[vx{i}]"
        )
        filter_parts.append(
            f"{last_a}[{i}:a]acrossfade=d={xfade_s}[ax{i}]"
        )
        last_v = f"[vx{i}]"
        last_a = f"[ax{i}]"
        cumulative += durations[i] - xfade_s

    filter_complex = ";".join(filter_parts)

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", last_v, "-map", last_a,
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "128k",
        str(output),
    ]
    emit_status("ffmpeg", cmd=" ".join(cmd[:8]) + " ... [filter_complex elided]")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        fail("FFMPEG_XFADE_FAILED", result.stderr[-1000:])


def main() -> None:
    args = parse_args()
    ffmpeg_check()

    if not args.run_dir.exists():
        fail("RUN_DIR_MISSING", f"{args.run_dir} does not exist")

    output = args.output or (args.run_dir / "final.mp4")
    if output.exists() and not args.force:
        emit_status("skip", reason="final.mp4 exists; use --force to overwrite", path=str(output))
        print(json.dumps({"final": str(output), "skipped": True}))
        return

    shot_dirs = sorted(d for d in args.run_dir.glob("shot-*") if d.is_dir())
    takes: list[Path] = []
    for sd in shot_dirs:
        t = pick_take(sd)
        if t is None:
            emit_status("warn", message="no usable take, skipping shot", shot=sd.name)
            continue
        takes.append(t)

    if not takes:
        fail("NO_TAKES", "no usable takes found in any shot directory")

    emit_status("assembling", shots=len(takes), output=str(output), xfade_ms=args.crossfade_ms)

    if args.crossfade_ms > 0:
        concat_with_xfade(takes, output, args.crossfade_ms)
    else:
        concat_hard_cut(takes, output)

    emit_status("done", final=str(output), shots=len(takes))
    print(json.dumps({"final": str(output), "shots": len(takes)}))


if __name__ == "__main__":
    main()
