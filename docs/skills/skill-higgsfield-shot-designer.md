---
name: higgsfield-shot-designer
description: Guide users through crafting effective Higgs Field AI video prompts by clarifying creative intent. Use when working with Higgs Field video generation, AI video prompting, shot design, Cinema Studio, Kling, or Veo workflows. Helps translate a vague creative idea into a structured prompt that covers what the text field actually controls — subject, scene, action, mood, lighting, and style — without wasting words on things the UI already handles.
---

# Higgs Field Shot Designer

A guided workflow for designing effective Higgs Field video prompts. Works by separating what the **UI controls** from what the **prompt controls**, then helping you think through the creative intent that only the prompt can express.

## How to Use This

**If you're an AI assistant:** Don't dump this whole document at the user. Walk them through it conversationally. Ask which workflow mode they're using, then ask the guided questions one at a time to draw out their creative intent. Output a clean prompt at the end.

**If you're a person:** Use the guided questions to think through your shot before you type anything into Higgs Field. The prompt structure and examples show you what to aim for.

## The Core Rule

**UI handles mechanics. Prompt handles content and emotional arc.**

The Higgs Field UI already controls: camera body, lens, focal length, aperture, duration, resolution, aspect ratio, camera movement presets, speed ramping, shot count, and genre pacing. Putting these in your text prompt is redundant at best, contradictory at worst.

The text prompt controls: what's in frame, what changes over time, camera *feel*, lighting, mood, style, and narrative beats.

## Prompt Structure

Follow this order for any shot prompt:

> **Subject → Scene → Action → Camera Feel → Lighting → Style**

Not every prompt needs all six. A start/end transition might only need camera feel. A narrative multi-shot scene needs all of them. Match depth to complexity.

## Workflow Modes

### Mode 1: Start/End Transitions

For creating smooth transitions between two frames (e.g. drone shot to interior, logo to product reveal).

**What matters most:** Frame selection. The start and end images do 80% of the work. The prompt is for minor steering.

**Prompt should be short (1-2 lines):**
- Camera behaviour: "gentle push-in", "handheld sway", "smooth arc"
- Continuity cues: "soft lighting carryover", "cinematic continuity"
- Small tweaks: colour shifts, subtle environment changes

**Prompt should NOT include:**
- Duration, resolution, aspect ratio (UI handles these)
- Complex narratives (the frames define the story)
- Camera hardware specs (irrelevant in this mode)

**Can go promptless.** Higgs Field infers motion path from the frames alone. Only add a prompt if you want to steer the transition feel.

**Frame selection tips:** The start and end frames are everything in this mode. For best results, use frames with similar orientation, lighting conditions, and subject positioning. Don't expect prompts to fix wildly different compositions — if the frames don't match well, no prompt will save it.

**Good examples:**
- `gentle push-in, cinematic continuity, soft lighting carryover`
- `smooth camera arc, golden hour warmth carries through`
- `subtle morph, keep eye line steady, minimal camera sway`

### Mode 2: Single Shot (with reference image)

For creating a video sequence from one reference image — product shots, B-roll, scene extensions.

**Think through:**
1. **Subject** — What's the focus? Be specific about the key element.
2. **Action** — What moves or changes? Character actions, environmental shifts, object motion.
3. **Camera feel** — Not the technical move (that's in the UI), but the *energy*. "Patient and slow" vs "urgent and handheld" vs "dreamlike float."
4. **Lighting/mood** — Time of day, light quality, emotional tone. This is where prompts add the most value.
5. **Style** — Photorealistic, cinematic, painterly, film era. Only if relevant.

**Good example:**
```
A woman in a white linen dress walks slowly along the deck of a yacht at sunset. 
Warm golden light catches the fabric. The ocean is calm, deep blue fading to amber 
at the horizon. Intimate, unhurried mood.
```

**Bad example (redundant with UI):**
```
Shot on RED V-Raptor 8K, 35mm anamorphic lens, f/2.8, 4K resolution, 
16:9 aspect ratio, slow dolly movement, 5 second duration. Woman on yacht.
```

### Mode 3: Auto Multi-Shot

For letting the AI generate multiple shots from one description. Works best with Kling 3.0.

**Write one coherent paragraph, not a shot list.** Use soft temporal cues: "first", "then", "as it builds", "finally."

**Think through:**
1. **The scene** — Where are we? What's the world?
2. **The arc** — What happens from beginning to end? What changes?
3. **Camera energy** — Overall feel, not per-shot specifics. "Dynamic handheld coverage" or "slow, graceful movements."
4. **Mood progression** — Does the energy build? Shift? Stay steady?

**Good example:**
```
Two friends argue in a small neon-lit diner at night. First, we see a wide 
establishing shot of the empty street outside. Then inside, close-ups as their 
argument intensifies, camera slowly circling the table. Finally, a quiet overhead 
shot — both in silence as neon reflections flicker on the table.
```

### Mode 4: Manual Multi-Shot (per-shot prompting)

For Cinema Studio or Kling 3.0 scene-based generation where each shot has its own prompt field.

**Each shot prompt is independent** — follow the Subject → Scene → Action → Camera Feel → Lighting → Style structure for each.

**Key rules:**
- Set duration, camera movement, and speed per shot in the UI
- Keep camera text high-level ("slow dolly in", "static overhead") since the UI controls the mechanics
- Reuse character names, key props, and environment descriptions across shots for continuity
- Mention physical details that matter for realism: cloth movement in wind, reflections, weight shifts

## Guided Questions

When you're stuck on what to prompt, work through these:

1. **What am I looking at?** — The subject, the environment, the key objects.
2. **What happens?** — The action, the change, the movement over time.
3. **How does it feel?** — The mood, the emotion, the energy level.
4. **What's the light doing?** — Time of day, quality (soft/harsh/dramatic), colour temperature.
5. **Is there a style reference?** — Film era, genre, visual language. Only if it matters.

If you can answer questions 1-3 clearly, you have a good prompt. Questions 4-5 refine it.

## Model Notes

- **Kling 3.0** — Best for narrative, multi-shot, dialogue. Responds well to scene structure, cinematic shot language, continuity prompts, and physics-aware details (cloth, hair, fluids). Supports prompted dialogue with native audio.
- **Veo 3.1** — Best for single shots, B-roll, reference-driven work. Shines with multiple reference images. Prompts should describe subtle continuous movement, not complex editorial structures.
- **Kling 2.5 Turbo** — More preset-driven. Simple motion and subject behaviour prompts. Don't over-prompt.

## The Auto-Enhance Toggle

Higgs Field has a "Prompt Enhance" toggle that rewrites your short prompt into a longer, more detailed version before sending it to the model.

- **Short prompt + enhance ON:** Good for quick exploration. Write your core idea in 1-2 lines, let the AI expand it. Works well when you're not sure exactly what you want yet.
- **Detailed prompt + enhance OFF:** Better for precision. When you've thought through your shot and written a specific prompt, turn enhance off so it doesn't override your choices.
- **Sometimes enhance OFF with a simple prompt gets better results** — the AI's expansion can over-specify and introduce unwanted elements. If your results feel "busy" or off-target, try turning it off.

Rule of thumb: start with enhance on while exploring, switch it off once you know what you want.

## Common Mistakes

- **Restating UI settings in the prompt** — Camera body, lens, focal length, aperture, duration, resolution, aspect ratio are all UI-controlled. Mentioning them wastes tokens and can create conflicts.
- **Over-prompting transitions** — Start/end frame workflows are frame-driven. A 5-word prompt or no prompt often beats a paragraph.
- **Using SHOT 1 / SHOT 2 format in auto multi-shot** — Use natural temporal language instead. Save explicit shot lists for manual/scene-based modes.
- **Describing what the camera does instead of what the scene feels like** — The UI sets the camera move. The prompt should convey the *emotional quality* of the movement, not the technical specification.
