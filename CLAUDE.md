# Carpet photo pipeline

Turns plain carpet photos into marketing shots (studio flat, rolled, room scenes) through the
OpenArt or Higgsfield connector: Nano Banana Pro, image-to-image, pattern preserved.

**Any request to generate shots/photos/images/scenes for carpets or rugs: invoke the
`carpet-shots` skill.** It asks the settings every time and runs the flow. This file holds the
connector recipes and rules the skill refers to.

## Connector recipes

### OpenArt (`mcp__claude_ai_OpenArt__*`)
Once per carpet, upload the source file directly (verified 2026-09-23; `openart_upload_import` no
longer takes URLs):
1. `openart_upload_sign(mediaType="image", contentType="image/jpeg", size=<bytes of carpet.src>,
   filename=<basename>, label=<carpet.name>, purpose="create-image")` -> `uploadId`, `signURL`, `accessURL`.
2. `curl -s -o /dev/null -w "%{http_code}" -X PUT -H "Content-Type: image/jpeg" --data-binary @"<carpet.src>" "<signURL>"`
   (expect 200).
3. `openart_upload_metadata_get(mediaUrl=<accessURL>, mediaType="image", uploadId=<uploadId>, label=<carpet.name>)`
   -> use its `visualReference` (`{type:"image", id, url, label}`) for every shot of that carpet.
Per shot: `openart_generate_image` (all shots of a carpet can be submitted at once, then waited on) with
```
model: "nano-banana-pro" (40 cr/image), mode: "image2image",
params: {"prompt": <shot.prompt verbatim>, "imageCount": 1, "aspectRatio": "3:2", "resolution": "1K",
         "autoEnhancePrompt": false,
         "visualReferences": [{"type": "image", "id": <id>, "url": <url>, "label": <carpet.name>}]}
```
Then `openart_creation_wait(historyId, timeoutSeconds=90)`; on STILL_RUNNING call it again (up to 4x).
On COMPLETED the image is `resources[0].url`. 1K output is 1264x848, plenty for web listings; 2K costs the
same 40 credits, so use "2K" only if the user asks for print-size files.

### Higgsfield (`mcp__claude_ai_Higsfield__*` or `mcp__higgsfield__*`)
Once per carpet: `media_import_url(url=<carpet.url>, type="image")` -> `media_id`.
Per shot: `generate_image` with
```
{"model": "nano_banana_pro", "prompt": <shot.prompt verbatim>, "aspect_ratio": "3:2", "count": 1,
 "resolution": "2k", "medias": [{"role": "image", "value": <media_id>}]}
```
Returns `results[0].id` = jobId. `job_status(jobId, sync=true)` until terminal (up to 5x).
On completed the image is `generation.results.rawUrl`. 2 credits per image (verified in the
transaction history, Sep 2026). Preferred connector when both are available.

## Rules
- Use `shot.prompt` from jobs.json verbatim. Do not shorten, translate, or "improve" it.
- Output paths are fixed by jobs.json (`<folder>/shots/<carpet>/<carpet>-NN-<scene>.jpg`); skip files that exist.
- Do not look at generated images during the batch, only at the test gate or when asked.
- Stop on any error mentioning credits, balance, quota or payment; report where you stopped.
- Resume = `python status.py --json` and continue with what is left.
- Never commit carpet photos, outputs, jobs.json or .urls.json.
