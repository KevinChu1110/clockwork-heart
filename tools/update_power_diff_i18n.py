import json

locales = {
    "zh_TW": {
        "防具": "防具",
        "防禦": "防禦",
        "攻擊": "攻擊",
        "攻擊 +%d": "攻擊 +%d",
        "防禦 +%d": "防禦 +%d",
    },
    "zh_CN": {
        "防具": "防具",
        "防禦": "防御",
        "攻擊": "攻击",
        "攻擊 +%d": "攻击 +%d",
        "防禦 +%d": "防御 +%d",
    },
    "en": {
        "防具": "Armour",
        "防禦": "DEF",
        "攻擊": "Attack",
        "攻擊 +%d": "ATK +%d",
        "防禦 +%d": "DEF +%d",
    },
    "ja": {
        "防具": "防具",
        "防禦": "防御",
        "攻擊": "攻撃",
        "攻擊 +%d": "攻撃 +%d",
        "防禦 +%d": "防御 +%d",
    },
    "ko": {
        "防具": "방어구",
        "防禦": "방어",
        "攻擊": "공격",
        "攻擊 +%d": "공격 +%d",
        "防禦 +%d": "방어 +%d",
    },
    "es": {
        "防具": "Armadura",
        "防禦": "DEF",
        "攻擊": "Ataque",
        "攻擊 +%d": "ATQ +%d",
        "防禦 +%d": "DEF +%d",
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
