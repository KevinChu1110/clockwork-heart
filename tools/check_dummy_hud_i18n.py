import json

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
keys = [
    "木人樁",
    "木人樁不反擊　·　自由試刀　·　右上可結束",
    "小白",
    "鎖定",
    "換武",
    "技能",
    "暫停",
    "攻擊",
    "結束試招"
]

base_path = "/opt/side/bravesoul-game/game/data/i18n/content"
for k in keys:
    print(f"=== Key: {k} ===")
    for loc in locales:
        p = f"{base_path}/{loc}/ui.json"
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        val = data.get(k, "<MISSING>")
        print(f"  [{loc}]: {val}")
