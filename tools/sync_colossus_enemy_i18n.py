#!/usr/bin/env python3
import json

data = {
    "zh_TW": {
        "colossus_lion": {"name": "失控發條獅"},
        "colossus_puppet": {"name": "霧鐘提線人偶"},
        "colossus_elephant": {"name": "黑鏽蒸氣巨象"}
    },
    "zh_CN": {
        "colossus_lion": {"name": "失控发条狮"},
        "colossus_puppet": {"name": "雾钟提线人偶"},
        "colossus_elephant": {"name": "黑锈蒸气巨象"}
    },
    "en": {
        "colossus_lion": {"name": "Rampant Clockwork Lion"},
        "colossus_puppet": {"name": "Mistbell Marionette"},
        "colossus_elephant": {"name": "Black-Rust Steam Colossus"}
    },
    "ja": {
        "colossus_lion": {"name": "暴走のぜんまい獅子"},
        "colossus_puppet": {"name": "霧鐘の操り人形"},
        "colossus_elephant": {"name": "黒錆の蒸気巨象"}
    },
    "ko": {
        "colossus_lion": {"name": "폭주 태엽 사자"},
        "colossus_puppet": {"name": "안개종 꼭두각시 인형"},
        "colossus_elephant": {"name": "검은녹 증기 거상"}
    },
    "es": {
        "colossus_lion": {"name": "León de Cuerda Desbocado"},
        "colossus_puppet": {"name": "Marioneta de Reloj de Niebla"},
        "colossus_elephant": {"name": "Coloso de Vapor de Óxido Negro"}
    }
}

for lang, entries in data.items():
    p = f"game/data/i18n/content/{lang}/enemy.json"
    try:
        with open(p, "r", encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        d = {}
    for k, v in entries.items():
        d[k] = v
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Updated {p}")
