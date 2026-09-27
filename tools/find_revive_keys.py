import json

base_path = "/opt/side/bravesoul-game/game/data/i18n/content/zh_CN/ui.json"
with open(base_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for k, v in data.items():
    if "复活" in v or "复活" in k or "战败" in k or "败北" in k:
        print(f"Key: {k} -> {v}")
