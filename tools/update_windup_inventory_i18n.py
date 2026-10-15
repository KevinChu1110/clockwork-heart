#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

locales = {
    "zh_TW": {
        "windup_daily.btn_go_inventory": "前往背包",
    },
    "zh_CN": {
        "windup_daily.btn_go_inventory": "前往背包",
    },
    "en": {
        "windup_daily.btn_go_inventory": "To Inventory",
    },
    "ja": {
        "windup_daily.btn_go_inventory": "バッグへ",
    },
    "ko": {
        "windup_daily.btn_go_inventory": "가방으로 이동",
    },
    "es": {
        "windup_daily.btn_go_inventory": "Ir a Mochila",
    }
}

base_path = "/opt/side/bravesoul-game/game/data/i18n"

for loc, kvs in locales.items():
    # 1. <loc>.json
    f1 = f"{base_path}/{loc}.json"
    with open(f1, "r", encoding="utf-8") as f:
        d1 = json.load(f)
    d1.update(kvs)
    with open(f1, "w", encoding="utf-8") as f:
        json.dump(d1, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # 2. content/<loc>/ui.json
    f2 = f"{base_path}/content/{loc}/ui.json"
    with open(f2, "r", encoding="utf-8") as f:
        d2 = json.load(f)
    d2.update(kvs)
    with open(f2, "w", encoding="utf-8") as f:
        json.dump(d2, f, ensure_ascii=False, indent=2)
        f.write("\n")

print("i18n updated successfully for windup_daily inventory button!")
