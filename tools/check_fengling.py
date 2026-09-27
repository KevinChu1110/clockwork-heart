import json

langs = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
for lang in langs:
    p = f"/opt/side/bravesoul-game/game/data/i18n/content/{lang}/ui.json"
    with open(p, "r", encoding="utf-8") as f:
        d = json.load(f)
        print(f"{lang} 封靈 -> {d.get('封靈')}")
