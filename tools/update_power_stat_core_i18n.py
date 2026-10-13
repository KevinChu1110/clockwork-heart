import json

locales = {
    "zh_TW": {
        "前往校準": "前往校準",
        "機芯總加成: 攻+%d · 防+%d · 血+%d": "機芯總加成: 攻+%d · 防+%d · 血+%d",
        "機芯加成": "機芯加成",
        "攻+%d · 防+%d · 血+%d": "攻+%d · 防+%d · 血+%d",
    },
    "zh_CN": {
        "前往校準": "前往校准",
        "機芯總加成: 攻+%d · 防+%d · 血+%d": "机芯总加成: 攻+%d · 防+%d · 血+%d",
        "機芯加成": "机芯加成",
        "攻+%d · 防+%d · 血+%d": "攻+%d · 防+%d · 血+%d",
    },
    "en": {
        "前往校準": "Calibrate",
        "機芯總加成: 攻+%d · 防+%d · 血+%d": "Core Total: ATK+%d · DEF+%d · HP+%d",
        "機芯加成": "Core Bonus",
        "攻+%d · 防+%d · 血+%d": "ATK+%d · DEF+%d · HP+%d",
    },
    "ja": {
        "前往校準": "較正へ",
        "機芯總加成: 攻+%d · 防+%d · 血+%d": "コア合計加成: 攻+%d · 防+%d · HP+%d",
        "機芯加成": "コア加成",
        "攻+%d · 防+%d · 血+%d": "攻+%d · 防+%d · HP+%d",
    },
    "ko": {
        "前往校準": "교정하러 가기",
        "機芯總加成: 攻+%d · 防+%d · 血+%d": "코어 총 보너스: 공+%d · 방+%d · 체+%d",
        "機芯加成": "코어 보너스",
        "攻+%d · 防+%d · 血+%d": "공+%d · 방+%d · 체+%d",
    },
    "es": {
        "前往校準": "Calibrar",
        "機芯總加成: 攻+%d · 防+%d · 血+%d": "Total de Núcleo: ATQ+%d · DEF+%d · PV+%d",
        "機芯加成": "Bonus de Núcleo",
        "攻+%d · 防+%d · 血+%d": "ATQ+%d · DEF+%d · PV+%d",
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

print("i18n updated successfully")
