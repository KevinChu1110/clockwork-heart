#!/usr/bin/env python3
import json

data = {
    "en": {
        "colossus_lion": {"name": "Rampant Clockwork Lion"},
        "colossus_puppet": {"name": "Mistbell Marionette"},
        "colossus_elephant": {"name": "Black Spindle Steam Colossus"}
    },
    "zh_CN": {
        "colossus_lion": {"name": "失控发条狮"},
        "colossus_puppet": {"name": "雾钟提线人偶"},
        "colossus_elephant": {"name": "黑镝蒸汽巨象"}
    },
    "ja": {
        "colossus_lion": {"name": "暴走のぜんまい獅子"},
        "colossus_puppet": {"name": "霧鐘の操り人形"},
        "colossus_elephant": {"name": "黒鏑の蒸気巨象"}
    },
    "ko": {
        "colossus_lion": {"name": "폭주 태엽 사자"},
        "colossus_puppet": {"name": "안개종 꼭두각시 인형"},
        "colossus_elephant": {"name": "흑적 증기 거상"}
    },
    "es": {
        "colossus_lion": {"name": "León de Cuerda Desbocado"},
        "colossus_puppet": {"name": "Marioneta del Reloj de Niebla"},
        "colossus_elephant": {"name": "Coloso de Vapor de Husillo Negro"}
    }
}

for lang, entries in data.items():
    p = f"game/data/i18n/content/{lang}/enemy.json"
    with open(p, "r", encoding="utf-8") as f:
        d = json.load(f)
    for k, v in entries.items():
        d[k] = v
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Updated {p}")
