import json

locales = {
    "zh_TW": {
        "調整心法": "調整心法"
    },
    "zh_CN": {
        "調整心法": "调整心法"
    },
    "en": {
        "調整心法": "Adjust Skills"
    },
    "ja": {
        "調整心法": "心法調整"
    },
    "ko": {
        "調整心法": "심법 조정"
    },
    "es": {
        "調整心法": "Ajustar habilidades"
    }
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

print("調整心法 i18n updated successfully in all 6 locales!")
