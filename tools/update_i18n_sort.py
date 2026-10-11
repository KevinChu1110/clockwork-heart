import json

translations = {
    "zh_TW": {
        "一鍵整理": "一鍵整理",
        "已完成一鍵整理": "已完成一鍵整理",
        "寶石": "寶石",
        "武器": "武器",
        "裝備": "裝備"
    },
    "zh_CN": {
        "一鍵整理": "一键整理",
        "已完成一鍵整理": "已完成一键整理",
        "寶石": "宝石",
        "武器": "武器",
        "裝備": "装备"
    },
    "en": {
        "一鍵整理": "Auto-Sort",
        "已完成一鍵整理": "Auto-Sort Complete",
        "寶石": "Gem",
        "武器": "Weapon",
        "裝備": "Equipment"
    },
    "ja": {
        "一鍵整理": "一括整理",
        "已完成一鍵整理": "一括整理完了",
        "寶石": "宝石",
        "武器": "武器",
        "裝備": "装備"
    },
    "ko": {
        "一鍵整理": "자동 정리",
        "已完成一鍵整理": "자동 정리 완료",
        "寶石": "보석",
        "武器": "무기",
        "裝備": "장비"
    },
    "es": {
        "一鍵整理": "Organizar",
        "已完成一鍵整理": "Organización completa",
        "寶石": "Gema",
        "武器": "Arma",
        "裝備": "Equipo"
    }
}

base_path = "/opt/side/bravesoul-game/game/data/i18n"
for loc, mapping in translations.items():
    p1 = f"{base_path}/content/{loc}/ui.json"
    try:
        with open(p1, "r", encoding="utf-8") as f:
            d = json.load(f)
        d.update(mapping)
        with open(p1, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        print("Updated", p1)
    except Exception as e:
        print("Error", p1, e)

    p2 = f"{base_path}/{loc}.json"
    try:
        with open(p2, "r", encoding="utf-8") as f:
            d = json.load(f)
        d.update(mapping)
        with open(p2, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        print("Updated", p2)
    except Exception as e:
        print("Error", p2, e)
