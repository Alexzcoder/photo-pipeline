# Carpet photo pipeline

Give it a folder of plain carpet photos, get marketing shots: studio flat, rolled up, and the carpet
placed in living rooms, bedrooms, dining rooms, kids rooms and more, in the furniture style and
lighting you choose. Image-to-image with Nano Banana Pro, so the real pattern and colours are kept.
Claude Code drives it through your own Higgsfield or OpenArt account. Nothing to host, no API keys.

## Setup on Windows (once, about 15 minutes)

You need a Claude Pro or Max subscription (Claude Code is not on the free plan).

1. **Install Python.** Download from https://www.python.org/downloads/ and run it. On the first
   screen tick **"Add python.exe to PATH"**, then Install Now.
2. **Install Git for Windows.** https://git-scm.com/downloads/win, keep all defaults. This gives
   Claude a proper shell to run the scripts in.
3. **Install Claude Code.** Open PowerShell (Start menu, type "PowerShell") and paste:
   ```
   irm https://claude.ai/install.ps1 | iex
   ```
   Close PowerShell and open it again, then check with `claude --version`.
4. **Connect an image connector to your Claude account.** In the browser go to
   https://claude.ai/settings/connectors, add **Higgsfield** (preferred, cheapest) or **OpenArt**,
   and sign in to that service when asked. Images are billed to that account's credits.
5. **Get the pipeline.** In PowerShell:
   ```
   cd $HOME\Desktop
   git clone https://github.com/Alexzcoder/photo-pipeline.git
   cd photo-pipeline
   python -m pip install pillow
   ```
6. **Log in to Claude Code.** Still in that folder, run `claude`. A browser window opens; log in
   with the same Claude account that has the connector. When the prompt appears, type `/mcp` and
   check the connector is listed and connected (it may ask you to authorise once).

## Every time you use it

1. Put the carpet photos in any folder, for example `C:\Users\you\Desktop\new carpets`. Name each
   file with its size in metres: `1.6x2.3 blue.jpg`, `200x290 ottoman.jpg`. If a name has no size,
   Claude will ask you for it.
2. Open PowerShell, go to the pipeline folder and start Claude:
   ```
   cd $HOME\Desktop\photo-pipeline
   claude
   ```
3. Type, with your own folder path:
   ```
   /carpet-shots C:\Users\you\Desktop\new carpets
   ```
4. Answer the questions: which rooms, furniture style, lighting, shots per room, and whether the
   photos have a price banner on them. Claude tells you your credit balance and what the run costs.
5. Claude does the first carpet, tells you how it looks, and asks before running the rest.
6. Results land in `<your folder>\shots\<carpet>\`. At the end Claude reports the images made and the
   credits used. Interrupted? Start `claude` again and say "continue the pipeline".

## Options
- Scenes: studio, rolled, livingroom, bedroom, dining, entryway, office, readingnook, openplan, lounge, kitchen, kidsroom, playroom, nursery
- Styles: classic-oriental, modern-minimal, vintage-distressed, art-deco, botanical, scandi-soft, luxe-baroque, bold-contrast, kids
- Lighting: daylight, golden, evening, overcast

## Cost
Higgsfield: 2 credits per image on Nano Banana Pro. The Ultimate plan grants 1200 credits a month and
unused credits are wiped at the monthly reset, so that is about 600 images or 85 carpets a month that
are otherwise lost. Claude prefers Higgsfield when both connectors are present.
OpenArt: 40 credits per image. 7 shots per carpet, so a 100-carpet batch is 700 images: 1,400 Higgsfield
credits or 28,000 OpenArt credits. Claude states the balance before each run and the credits used at the end.

## Mac / Linux
Same steps with the Linux/macOS Claude installer (`curl -fsSL https://claude.ai/install.sh | bash`),
`python3` instead of `python` if `python` is not found, and `pip install pillow`.

## Files
`.claude/skills/carpet-shots/SKILL.md` is the interactive flow; `CLAUDE.md` holds the connector recipes and rules.
`prompts.py` holds the scene and style texts; edit it to change the look. `make_jobs.py` builds `jobs.json`,
`save_shot.py` downloads a result, `status.py` shows what's left.
