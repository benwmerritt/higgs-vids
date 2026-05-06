#!/usr/bin/env python3
"""compose-moodboard.py — assemble a moodboard run into a single branded PNG/PDF.

Reads:
  <run-dir>/structure.json             (slot order + treatment labels)
  <run-dir>/shot-NN/image.png          (the generated images)
  <run-dir>/shot-NN/treatment.txt      (slot label, optional)
  <run-dir>/direction-draft.md         (creative direction copy)
  <run-dir>/palette.md                 (observed palette, optional)
  brands/<brand>/profile.md            (brand name, voice for header)
  brands/<brand>/assets/logos/*.png    (brand mark, optional)

Outputs:
  <output>.png                         (composed moodboard, default 2400×3200)
  <output>.pdf                         (same content, PDF format)

This is the deliverable. Hand the PNG/PDF to a client; the per-shot images
are still in the run-dir if they want to review individually.

Dependencies: Pillow (PIL).
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import date

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError:
    sys.stderr.write(
        "Pillow not installed. Install: pip install Pillow\n"
    )
    sys.exit(2)


# ─── Layout constants (portrait 2400×3200) ──────────────────────────
CANVAS_W, CANVAS_H = 2400, 3200
MARGIN = 80
HEADER_H = 240
PALETTE_H = 140
DIRECTION_H = 480
FOOTER_H = 100

GRID_TOP = MARGIN + HEADER_H + 40
GRID_H = CANVAS_H - GRID_TOP - PALETTE_H - DIRECTION_H - FOOTER_H - 80
GRID_W = CANVAS_W - 2 * MARGIN

# Colours (used when brand colours unavailable)
BG = (250, 248, 244)          # warm off-white
INK = (28, 32, 38)              # near-black
MUTED = (120, 122, 124)
RULE = (210, 208, 200)


def find_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Find a usable system font. Falls back to Pillow default."""
    candidates = [
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size, index=1 if bold else 0)
            except Exception:
                try:
                    return ImageFont.truetype(path, size)
                except Exception:
                    continue
    return ImageFont.load_default()


def read_brand_name(brand_dir: Path) -> str:
    profile = brand_dir / "profile.md"
    if profile.exists():
        content = profile.read_text(encoding="utf-8")
        m = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
        if m:
            return m.group(1).strip()
        m = re.search(r"^# Brand:\s*(.+)$", content, re.MULTILINE)
        if m:
            return m.group(1).strip()
    return brand_dir.name.replace("-", " ").title()


def find_logo(brand_dir: Path) -> Path | None:
    logos_dir = brand_dir / "assets" / "logos"
    if not logos_dir.exists():
        return None
    for name in ("primary.png", "primary.svg", "logo.png", "logo.svg"):
        p = logos_dir / name
        if p.exists() and p.suffix == ".png":
            return p
    pngs = list(logos_dir.glob("*.png"))
    return pngs[0] if pngs else None


def read_direction(run_dir: Path) -> tuple[str, str]:
    """Returns (title, body). Title from first H1 or filename; body from prose."""
    direction = run_dir / "direction-draft.md"
    if not direction.exists():
        direction = run_dir / "direction.md"
    if not direction.exists():
        return ("Creative Direction", "")

    content = direction.read_text(encoding="utf-8")
    title_m = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else "Creative Direction"

    vision_m = re.search(r"##\s+The vision\s*\n+(.*?)(?=\n##|\Z)", content, re.DOTALL)
    if vision_m:
        body = vision_m.group(1).strip()
    else:
        lines = [l for l in content.splitlines()
                 if l.strip() and not l.lstrip().startswith("#")
                 and not l.lstrip().startswith(">")]
        body = " ".join(lines).strip()

    body = re.sub(r"\[.*?\]", "", body)
    body = re.sub(r"\s+", " ", body).strip()
    if len(body) > 600:
        body = body[:600].rsplit(" ", 1)[0] + "…"
    return title, body


def read_palette(run_dir: Path) -> list[tuple[int, int, int]]:
    """Returns up to 7 RGB tuples extracted from palette.md."""
    palette_file = run_dir / "palette.md"
    if not palette_file.exists():
        return []
    content = palette_file.read_text(encoding="utf-8")
    hex_matches = re.findall(r"#([0-9A-Fa-f]{6})", content)
    colours = []
    for h in hex_matches[:7]:
        colours.append((int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)))
    return colours


def read_shots(run_dir: Path) -> list[dict]:
    """Returns list of {id, image_path, treatment} for each shot folder."""
    shots = []
    for shot_dir in sorted(run_dir.glob("shot-*")):
        if not shot_dir.is_dir():
            continue
        img = shot_dir / "image.png"
        if not img.exists():
            continue
        treatment_file = shot_dir / "treatment.txt"
        treatment = treatment_file.read_text(encoding="utf-8").strip().splitlines()[0] \
            if treatment_file.exists() else ""
        shots.append({
            "id": shot_dir.name.replace("shot-", ""),
            "image": img,
            "treatment": treatment[:48],
        })
    return shots


def fit_image(src_path: Path, w: int, h: int) -> Image.Image:
    img = Image.open(src_path).convert("RGB")
    img = ImageOps.fit(img, (w, h), method=Image.Resampling.LANCZOS)
    return img


def draw_text_box(draw, text, xy, max_w, font, fill, line_spacing=8):
    """Wrap text to max_w pixels and draw at xy. Returns (lines_drawn, total_h)."""
    if not text:
        return (0, 0)
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = (current + " " + word).strip() if current else word
        bbox = font.getbbox(candidate)
        if bbox[2] - bbox[0] <= max_w:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)

    x, y = xy
    line_h = (font.getbbox("Ay")[3] - font.getbbox("Ay")[1]) + line_spacing
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += line_h
    return (len(lines), y - xy[1])


def compose_editorial_grid(canvas: Image.Image, shots: list[dict], top_y: int,
                            grid_w: int, grid_h: int, draw: ImageDraw.ImageDraw):
    """Editorial layout: 1 hero + N satellites. Adapts to 6/8/9 shots."""
    n = len(shots)
    if n == 0:
        return
    if n >= 7:
        hero_h = int(grid_h * 0.42)
        rows_h = grid_h - hero_h - 40
        hero = fit_image(shots[0]["image"], grid_w, hero_h)
        canvas.paste(hero, (MARGIN, top_y))
        if shots[0]["treatment"]:
            draw.text(
                (MARGIN + 16, top_y + hero_h - 50),
                shots[0]["treatment"].upper(),
                font=find_font(20),
                fill=(255, 255, 255),
            )

        rows = 2
        per_row = max(1, (n - 1 + rows - 1) // rows)
        cell_w = (grid_w - (per_row - 1) * 16) // per_row
        cell_h = (rows_h - 16) // rows
        sat = shots[1:]
        for i, shot in enumerate(sat):
            r = i // per_row
            c = i % per_row
            x = MARGIN + c * (cell_w + 16)
            y = top_y + hero_h + 40 + r * (cell_h + 16)
            img = fit_image(shot["image"], cell_w, cell_h)
            canvas.paste(img, (x, y))
            if shot["treatment"]:
                draw.text(
                    (x + 12, y + cell_h - 38),
                    shot["treatment"].upper(),
                    font=find_font(16),
                    fill=(255, 255, 255),
                )
    else:
        cols = 3 if n >= 5 else 2
        rows = (n + cols - 1) // cols
        cell_w = (grid_w - (cols - 1) * 16) // cols
        cell_h = (grid_h - (rows - 1) * 16) // rows
        for i, shot in enumerate(shots):
            r = i // cols
            c = i % cols
            x = MARGIN + c * (cell_w + 16)
            y = top_y + r * (cell_h + 16)
            img = fit_image(shot["image"], cell_w, cell_h)
            canvas.paste(img, (x, y))
            if shot["treatment"]:
                draw.text(
                    (x + 12, y + cell_h - 38),
                    shot["treatment"].upper(),
                    font=find_font(16),
                    fill=(255, 255, 255),
                )


def compose(run_dir: Path, brand_dir: Path, output: Path,
            client_name: str = "[Client Name]") -> None:
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), BG)
    draw = ImageDraw.Draw(canvas)

    brand_name = read_brand_name(brand_dir)
    logo_path = find_logo(brand_dir)
    direction_title, direction_body = read_direction(run_dir)
    palette_colours = read_palette(run_dir)
    shots = read_shots(run_dir)

    if not shots:
        sys.stderr.write(f"No shots found in {run_dir}\n")
        sys.exit(1)

    # ─── Header ──────────────────────────────────────────────────
    header_y = MARGIN
    if logo_path:
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo.thumbnail((180, 180), Image.Resampling.LANCZOS)
            canvas.paste(logo, (MARGIN, header_y),
                         logo if logo.mode == "RGBA" else None)
        except Exception:
            pass

    title_x = MARGIN + 220 if logo_path else MARGIN
    draw.text((title_x, header_y + 16),
              "MOODBOARD",
              font=find_font(28), fill=MUTED)
    draw.text((title_x, header_y + 60),
              direction_title.upper(),
              font=find_font(56, bold=True), fill=INK)
    draw.text((title_x, header_y + 140),
              f"For {client_name}  ·  {brand_name}  ·  {date.today().isoformat()}",
              font=find_font(22), fill=MUTED)

    rule_y = MARGIN + HEADER_H + 8
    draw.line([(MARGIN, rule_y), (CANVAS_W - MARGIN, rule_y)], fill=RULE, width=2)

    # ─── Image grid ─────────────────────────────────────────────
    compose_editorial_grid(canvas, shots, GRID_TOP, GRID_W, GRID_H, draw)

    # ─── Palette strip ──────────────────────────────────────────
    palette_y = GRID_TOP + GRID_H + 30
    draw.text((MARGIN, palette_y),
              "PALETTE",
              font=find_font(18), fill=MUTED)
    if palette_colours:
        swatch_y = palette_y + 38
        swatch_h = 80
        n = len(palette_colours)
        swatch_w = (CANVAS_W - 2 * MARGIN - (n - 1) * 12) // n
        for i, c in enumerate(palette_colours):
            x = MARGIN + i * (swatch_w + 12)
            draw.rectangle([x, swatch_y, x + swatch_w, swatch_y + swatch_h],
                           fill=c, outline=RULE, width=1)
            hex_label = "#{:02X}{:02X}{:02X}".format(*c)
            draw.text((x + 8, swatch_y + swatch_h + 6),
                      hex_label, font=find_font(14), fill=MUTED)
    else:
        draw.text((MARGIN, palette_y + 38),
                  "(palette will populate from generated images on next run)",
                  font=find_font(16), fill=MUTED)

    # ─── Direction copy ─────────────────────────────────────────
    direction_y = palette_y + PALETTE_H + 40
    draw.text((MARGIN, direction_y),
              "CREATIVE DIRECTION",
              font=find_font(18), fill=MUTED)
    if direction_body:
        draw_text_box(draw, direction_body,
                      (MARGIN, direction_y + 36),
                      CANVAS_W - 2 * MARGIN,
                      find_font(22), INK,
                      line_spacing=10)

    # ─── Footer ─────────────────────────────────────────────────
    footer_y = CANVAS_H - MARGIN - 30
    draw.text((MARGIN, footer_y),
              f"Higgsfield Autopilot  ·  {brand_name}  ·  {run_dir.name}",
              font=find_font(14), fill=MUTED)

    # ─── Save ────────────────────────────────────────────────────
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, "PNG", optimize=True)
    print(f"✓ {output}  ({CANVAS_W}×{CANVAS_H})")

    if output.suffix.lower() == ".png":
        pdf_path = output.with_suffix(".pdf")
        canvas.save(pdf_path, "PDF", resolution=150.0)
        print(f"✓ {pdf_path}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--run-dir", required=True, type=Path,
                   help="The moodboard run directory (e.g. runs/2026-05-07-ben-moodboard-1)")
    p.add_argument("--brand", required=True,
                   help="Brand name (looked up at brands/<brand>/profile.md)")
    p.add_argument("--output", type=Path,
                   help="Output PNG path. Default: <run-dir>/deliverables/moodboard.png")
    p.add_argument("--client", default="[Client Name]",
                   help="Client name for the header. Default: '[Client Name]' (placeholder).")
    p.add_argument("--brands-dir", type=Path, default=Path("brands"),
                   help="Where brand profiles live. Default: ./brands")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    run_dir = args.run_dir.resolve()
    if not run_dir.exists():
        sys.stderr.write(f"Run dir not found: {run_dir}\n")
        sys.exit(1)

    brand_dir = (args.brands_dir / args.brand).resolve()
    if not brand_dir.exists():
        sys.stderr.write(f"Brand dir not found: {brand_dir}\n"
                         f"  (Run /higgsfield-brand-create {args.brand} first.)\n")
        sys.exit(1)

    output = args.output or (run_dir / "deliverables" / "moodboard.png")
    output = output.resolve()

    compose(run_dir, brand_dir, output, client_name=args.client)


if __name__ == "__main__":
    main()
