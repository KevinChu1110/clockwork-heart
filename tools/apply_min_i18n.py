import json
import os

base_dir = "/opt/side/bravesoul-game/game/data/i18n/content"

TRANSLATIONS_MIN = {
    "zh_TW": {"%d分": "%d分"},
    "zh_CN": {"%d分": "%d分"},
    "en": {"%d分": "%d min"},
    "ja": {"%d分": "%d分"},
    "ko": {"%d分": "%d분"},
    "es": {"%d分": "%d min"},
}

for loc, items in TRANSLATIONS_MIN.items():
    p = os.path.join(base_dir, loc, "ui.json")
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    for k, v in items.items():
        data[k] = v
    sorted_data = dict(sorted(data.items(), key=lambda x: x[0]))
    with open(p, "w", encoding="utf-8") as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Updated {loc}/ui.json with %d分")
