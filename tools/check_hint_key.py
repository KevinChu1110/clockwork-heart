import json

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
k = "木人樁不反擊 · 自由試刀 · 右上可結束"
base_path = "/opt/side/bravesoul-game/game/data/i18n/content"
print(f"=== Key: {k} ===")
for loc in locales:
    p = f"{base_path}/{loc}/ui.json"
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    val = data.get(k, "<MISSING>")
    print(f"  [{loc}]: {val}")
