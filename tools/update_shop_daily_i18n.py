#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

locales = {
    "zh_TW": {
        "shop.btn_go_daily": "前往委託",
        "shop.btn_go_windup": "前往委託"
    },
    "zh_CN": {
        "shop.btn_go_daily": "前往委托",
        "shop.btn_go_windup": "前往委托"
    },
    "en": {
        "shop.btn_go_daily": "To Daily",
        "shop.btn_go_windup": "To Daily"
    },
    "ja": {
        "shop.btn_go_daily": "日課へ",
        "shop.btn_go_windup": "日課へ"
    },
    "ko": {
        "shop.btn_go_daily": "일일 의뢰로 이동",
        "shop.btn_go_windup": "일일 의뢰로 이동"
    },
    "es": {
        "shop.btn_go_daily": "Ir a Encargos",
        "shop.btn_go_windup": "Ir a Encargos"
    }
}

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../game/data/i18n"))

for loc, kvs in locales.items():
    # 1. <loc>.json
    f1 = f"{base_path}/{loc}.json"
    if os.path.exists(f1):
        with open(f1, "r", encoding="utf-8") as f:
            d1 = json.load(f)
        d1.update(kvs)
        with open(f1, "w", encoding="utf-8") as f:
            json.dump(d1, f, ensure_ascii=False, indent=2)
            f.write("\n")

    # 2. content/<loc>/ui.json
    f2 = f"{base_path}/content/{loc}/ui.json"
    if os.path.exists(f2):
        with open(f2, "r", encoding="utf-8") as f:
            d2 = json.load(f)
        d2.update(kvs)
        with open(f2, "w", encoding="utf-8") as f:
            json.dump(d2, f, ensure_ascii=False, indent=2)
            f.write("\n")

print("Shop daily shortcut i18n updated successfully!")
