import json

for lang in ["en", "ko", "es"]:
    p = f"/opt/side/bravesoul-game/game/data/i18n/{lang}.json"
    with open(p, "r", encoding="utf-8") as f:
        d = json.load(f)
        for k in ["daily.D1.body", "daily.D5.body", "hud.default_name"]:
            print(f"{lang} {k} -> {d.get(k)}")
