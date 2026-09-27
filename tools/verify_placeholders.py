import json
import re

PLACEHOLDER = re.compile(r"%[-+ #0-9.]*[sdfxXoc%]")

def placeholders(s: str) -> list:
    return [m.group(0) for m in PLACEHOLDER.finditer(s) if m.group(0) != "%%"]

for lc in ["en", "ja", "ko", "es", "zh_CN"]:
    path = f"/opt/side/bravesoul-game/game/data/i18n/content/{lc}/ui.json"
    data = json.load(open(path, encoding="utf-8"))
    for k, v in data.items():
        if placeholders(k) != placeholders(v):
            print(f"[{lc}] Mismatch:\n  src: {k}\n  tgt: {v}")
print("Placeholder check finished.")
