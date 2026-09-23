# Carpet photo pipeline

Give it a folder of plain carpet photos, get marketing shots: studio flat, rolled up, and the carpet
placed in living rooms, bedrooms, dining rooms, kids rooms and more, in the furniture style and
lighting you choose. Image-to-image, so the real pattern and colours are kept. Claude Code drives it
through your own OpenArt or Higgsfield account; nothing to host, no API keys.

## Setup (once, 10 minutes)
1. Install [Claude Code](https://claude.com/claude-code) and sign in.
2. Connect a connector in Claude: **OpenArt** or **Higgsfield** (Settings → Connectors). Either works;
   images are billed to that account's credits.
3. Install Python 3 and run `pip install pillow`. `curl` must be available (it is on Windows 10+, macOS, Linux).
4. Clone this repo.

## Use
1. Open a terminal in the repo folder, run `claude`, and type:
   > /carpet-shots C:\Users\me\Desktop\new carpets
2. Claude asks which rooms, style, lighting, shots per room, and whether the photos have a price
   banner on them. Name files with the size in metres (`1.6x2.3 blue.jpg`) or Claude will ask for sizes.
3. It does the first carpet, shows you the result, and asks before running the rest.
4. Results land in `<your folder>/shots/<carpet>/`. Interrupted? Run `claude` again and say "continue the pipeline".

## Options
- Scenes: studio, rolled, livingroom, bedroom, dining, entryway, office, readingnook, openplan, lounge, kitchen, kidsroom, playroom, nursery
- Styles: classic-oriental, modern-minimal, vintage-distressed, art-deco, botanical, scandi-soft, luxe-baroque, bold-contrast, kids
- Lighting: daylight, golden, evening, overcast

## Cost
Higgsfield: 2 credits per image on Nano Banana Pro (measured). The Ultimate plan grants 1200 credits a
month and unused credits are wiped at the monthly reset, so that is about 600 images or 85 carpets a
month that are otherwise lost. Claude prefers Higgsfield when both connectors are present.
OpenArt: 40 credits per image on Nano Banana Pro. 7 shots per carpet, so a 100-carpet batch is 700
images: 1,400 Higgsfield credits or 28,000 OpenArt credits. The model is always Nano Banana Pro.
Claude states the balance before each run and the credits used at the end.

## Files
`.claude/skills/carpet-shots/SKILL.md` is the interactive flow; `CLAUDE.md` holds the connector recipes and rules.
`prompts.py` holds the scene and style texts; edit it to change the look. `make_jobs.py` builds `jobs.json`,
`save_shot.py` downloads a result, `status.py` shows what's left.
