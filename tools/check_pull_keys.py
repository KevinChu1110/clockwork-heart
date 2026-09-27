import json

langs = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
for lang in ["zh_CN", "en", "ja", "ko", "es"]:
    p = f"/opt/side/bravesoul-game/game/data/i18n/{lang}.json"
    with open(p, "r", encoding="utf-8") as f:
        d = json.load(f)
        for k in ["soul.pull_part", "soul.pull_outfit", "soul.pull_junk"]:
            print(f"{lang} {k} -> {d.get(k)}")
