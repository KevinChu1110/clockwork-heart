import json

locales = {
    "zh_TW": {
        "已穿戴": "已穿戴",
        "穿戴中": "穿戴中",
    },
    "zh_CN": {
        "已穿戴": "已穿戴",
        "穿戴中": "穿戴中",
    },
    "en": {
        "已穿戴": "Equipped",
        "穿戴中": "Equipped",
    },
    "ja": {
        "已穿戴": "装備済み",
        "穿戴中": "装備中",
    },
    "ko": {
        "已穿戴": "장착됨",
        "穿戴中": "장착 중",
    },
    "es": {
        "已穿戴": "Equipado",
        "穿戴中": "Equipado",
    },
}

for loc, entries in locales.items():
    ui_path = f"/opt/side/bravesoul-game/game/data/i18n/content/{loc}/ui.json"
    with open(ui_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for k, v in entries.items():
        data[k] = v
    with open(ui_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    root_path = f"/opt/side/bravesoul-game/game/data/i18n/{loc}.json"
    with open(root_path, "r", encoding="utf-8") as f:
        data2 = json.load(f)
    for k, v in entries.items():
        data2[k] = v
    with open(root_path, "w", encoding="utf-8") as f:
        json.dump(data2, f, ensure_ascii=False, indent=2)
        f.write("\n")

print("Updated i18n files for all 6 locales successfully!")
