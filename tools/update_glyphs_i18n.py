#!/usr/bin/env python3
import json

GLYPHS = {
    "zh_TW": {"板": "板", "軸": "軸"},
    "zh_CN": {"板": "板", "軸": "轴"},
    "en": {"板": "P", "軸": "A"},
    "es": {"板": "P", "軸": "E"},
    "ja": {"板": "板", "軸": "軸"},
    "ko": {"板": "판", "軸": "축"},
}

for loc, entries in GLYPHS.items():
    p = f"/opt/side/bravesoul-game/game/data/i18n/content/{loc}/ui.json"
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    for k, v in entries.items():
        data[k] = v
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print(f"Updated {loc}/ui.json with 板 and 軸")
