# Download a generated image to an exact path as JPEG.   Usage: python save_shot.py <url> <out.jpg>
import io, os, sys, time, urllib.request
from PIL import Image

url, out = sys.argv[1], sys.argv[2]
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
for attempt in range(4):   # CDNs throw the odd timeout; a retry is cheaper than a regeneration
    try:
        b = urllib.request.urlopen(req, timeout=120).read(); break
    except Exception as e:
        if attempt == 3: raise
        print("retry", attempt + 1, e); time.sleep(3 * (attempt + 1))
Image.open(io.BytesIO(b)).convert("RGB").save(out, "JPEG", quality=92)
print("saved", out)
