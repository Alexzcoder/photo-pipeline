# Build jobs.json: one entry per carpet image in a folder, with public URL (catbox) + prompts per shot.
# Usage: python make_jobs.py <folder> --scenes studio,livingroom,bedroom,dining,office,entryway,rolled
#                             --style scandi-soft --light daylight [--per 1] [--banner] [--no-upload]
# Sizes (metres) come from the filename ("1.6x2.3 red.jpg", "160x230.jpg") or from <folder>/sizes.csv (name,w,l).
# Resumable: uploads are cached in .urls.json.
import argparse, csv, glob, io, json, os, re, subprocess, sys, time
from PIL import Image
from prompts import build_prompts, ORDER, STYLES, LIGHTS

ap = argparse.ArgumentParser()
ap.add_argument("folder"); ap.add_argument("--scenes", default="studio,livingroom,bedroom,dining,office,entryway,rolled")
ap.add_argument("--style", default="scandi-soft", choices=list(STYLES)); ap.add_argument("--light", default="daylight", choices=list(LIGHTS))
ap.add_argument("--per", type=int, default=1); ap.add_argument("--banner", action="store_true")
ap.add_argument("--out", default=None, help="default: <folder>/shots"); ap.add_argument("--no-upload", action="store_true", help="prompts only, for a dry run")
a = ap.parse_args()
a.out = a.out or os.path.join(a.folder, "shots")
scenes = [s for s in ORDER if s in a.scenes.split(",")]
bad = set(a.scenes.split(",")) - set(ORDER)
if bad: sys.exit(f"unknown scenes {sorted(bad)}; choose from {ORDER}")

sizes = {}
csvp = os.path.join(a.folder, "sizes.csv")
if os.path.exists(csvp):
    for row in csv.reader(open(csvp)):
        if len(row) >= 3 and row[1].replace(".", "").isdigit(): sizes[os.path.splitext(row[0])[0]] = (float(row[1]), float(row[2]))

def size_of(name):
    if name in sizes: return sizes[name]
    m = re.search(r"(\d+(?:[.,]\d+)?)\s*[x×]\s*(\d+(?:[.,]\d+)?)", name)
    if not m: return None
    w, l = float(m[1].replace(",", ".")), float(m[2].replace(",", "."))
    return (w / 100, l / 100) if w > 10 else (w, l)

cache_p = ".urls.json"; cache = json.load(open(cache_p)) if os.path.exists(cache_p) else {}
def upload(path):
    if path in cache: return cache[path]
    import tempfile
    small = os.path.join(tempfile.gettempdir(), "_carpet_up.jpg")
    im = Image.open(path).convert("RGB"); im.thumbnail((1600, 1600)); im.save(small, "JPEG", quality=88)
    for attempt in range(5):   # catbox rate-limits; back off
        p = subprocess.run(["curl", "-sS", "-m", "90", "-F", "reqtype=fileupload", "-F", f"fileToUpload=@{small}",
                            "https://catbox.moe/user/api.php"], capture_output=True, text=True)
        if p.stdout.strip().startswith("https://"):
            cache[path] = p.stdout.strip(); json.dump(cache, open(cache_p, "w"), indent=1); return cache[path]
        time.sleep(3 * (attempt + 1))
    sys.exit(f"upload failed for {path}: {p.stdout[:100]} {p.stderr[:100]}")

files = sorted(f for f in glob.glob(os.path.join(a.folder, "*")) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")))
if not files: sys.exit(f"no images in {a.folder}")
carpets, missing = [], []
for f in files:
    name = os.path.splitext(os.path.basename(f))[0]
    sz = size_of(name)
    if not sz: missing.append(name); continue
    w, l = sz
    shots = [{"key": k, "file": os.path.join(a.out, name, f"{name}-{i+1:02d}-{k}" + (f"-v{v}" if v > 1 else "") + ".jpg"), "prompt": p}
             for i, (k, p) in enumerate(build_prompts(w, l, scenes, a.style, a.light, a.banner).items()) for v in range(1, a.per + 1)]
    carpets.append({"name": name, "src": os.path.abspath(f), "w": w, "l": l, "url": None if a.no_upload else upload(f), "shots": shots})
    print(f"{name}: {w}x{l} m, {len(shots)} shots" + ("" if a.no_upload else f", {carpets[-1]['url']}"))
if missing: sys.exit(f"no size for {missing}: rename to include WxL (e.g. '1.6x2.3 {missing[0]}.jpg') or add rows to {csvp}")
json.dump({"settings": vars(a) | {"scenes": scenes}, "carpets": carpets}, open("jobs.json", "w"), ensure_ascii=False, indent=1)
print(f"wrote jobs.json: {len(carpets)} carpets, {sum(len(c['shots']) for c in carpets)} images")
