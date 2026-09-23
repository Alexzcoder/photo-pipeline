---
name: carpet-shots
description: Generate marketing shots (studio, rolled, room scenes) for a folder of carpet photos through the OpenArt or Higgsfield connector. Use when the user asks to generate shots, photos, images or scenes for carpets/rugs, or runs /carpet-shots <folder>.
---

# /carpet-shots <folder>

The argument is the folder holding the carpet photos (any path; drag-and-drop paths work).
If no folder was given, ask for it first. Outputs go to `<folder>/shots/<carpet>/`.

## 1. Always ask, every task
Use AskUserQuestion. Never reuse answers from a previous run; ask again each time.

- **Rooms/scenes** (multi-select): studio, rolled, livingroom, bedroom, dining, entryway, office,
  readingnook, openplan, lounge, kitchen, kidsroom, playroom, nursery. Recommend
  studio + livingroom + bedroom + dining + rolled.
- **Furniture style**: classic-oriental, modern-minimal, vintage-distressed, art-deco, botanical,
  scandi-soft, luxe-baroque, bold-contrast, kids.
- **Lighting**: daylight, golden, evening, overcast.
- **Shots per scene**: 1, 2 or 3.
- **Price banner burned into the source photos?** yes/no.

Then check sizes: list the image files in the folder. Any filename without `WxL` metres
(e.g. `1.6x2.3 blue.jpg`, `160x230.jpg`) and no row in `<folder>/sizes.csv` needs a size.
Ask for those sizes in one question (one line per file) and write them to `<folder>/sizes.csv`
as `name,w,l`. Do not guess sizes.

Connector: use whichever of OpenArt / Higgsfield tools you have. If both, prefer Higgsfield:
Nano Banana Pro costs 2 credits there and the plan's 1200 monthly credits do not roll over, so
they are use-it-or-lose-it. Only fall back to OpenArt when Higgsfield's balance cannot cover the
run (2 x images). Model is always Nano Banana Pro on either connector (decided 2026-09-23; the
cheaper Nano Banana 2 / 2 Lite were tested and rejected).

## 1b. Credits before
Fetch the balance and tell the user before generating anything:
OpenArt `openart_account_get` -> credits; Higgsfield `balance`. Say: "You have N credits.
This run is M images." Remember N.

## 2. Build
`python3 make_jobs.py "<folder>" --scenes a,b,c --style X --light Y --per N [--banner]`
It uploads the sources to a public host and writes `jobs.json`. Read it for the shot list.

## 3. Test gate
Generate all shots of the first carpet only (recipes in CLAUDE.md), save each with
`python3 save_shot.py "<url>" "<shot.file>"`, then Read the saved images (no contact sheet needed)
and tell the user in three lines whether the pattern is kept, the scale looks real, and there is
no text/banner. Name the output folder so they can look themselves.
Ask: continue with the rest, change settings (go back to step 1), or stop.

## 4. Batch
Only after an explicit yes. Per carpet, per shot: skip if the file exists, generate, save.
More than 5 carpets: split into 3 or 4 ranges and run parallel subagents, each with the
CLAUDE.md recipe and its range. Stop everything on any credits/balance/quota/payment error.

## 5. Report
`python3 status.py`, then fetch the balance again. Report: images done, folder path, failures, and
"This run used X credits (N before, now N-X left)". Never claim done without status.py and the
credit line. If the user stops at the test gate, give the same credit line for what was spent.
