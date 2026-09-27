import json

langs = ["zh_CN", "en", "ja", "ko", "es"]
for lang in langs:
    p = f"/opt/side/bravesoul-game/game/data/i18n/{lang}.json"
    with open(p, "r", encoding="utf-8") as f:
        d = json.load(f)
        for k, v in d.items():
            if "小白" in k or "小白" in str(v):
                print(f"{lang} {k} -> {v}")
