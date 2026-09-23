# What is still missing from jobs.json.   Usage: python3 status.py [--json] [--carpet NAME]
import json, os, sys

j = json.load(open("jobs.json")); want = sys.argv[sys.argv.index("--carpet") + 1] if "--carpet" in sys.argv else None
todo = {c["name"]: [s for s in c["shots"] if not os.path.exists(s["file"])] for c in j["carpets"] if not want or c["name"] == want}
left = sum(len(v) for v in todo.values()); total = sum(len(c["shots"]) for c in j["carpets"] if not want or c["name"] == want)
if "--json" in sys.argv:
    print(json.dumps({"left": left, "total": total, "carpets": {k: [s["key"] for s in v] for k, v in todo.items() if v}}, indent=1))
else:
    for k, v in todo.items(): print(f"{k}: {'complete' if not v else 'missing ' + ', '.join(s['key'] for s in v)}")
    print(f"{total - left}/{total} images done, {left} left")
