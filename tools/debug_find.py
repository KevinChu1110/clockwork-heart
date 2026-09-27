import json

p = "/opt/side/bravesoul-game/game/data/i18n/zh_TW.json"
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)
    for k, v in d.items():
        if any(x in k for x in ["soul", "drop", "gear", "outfit", "junk"]):
            print(f"{k}: {v}")
