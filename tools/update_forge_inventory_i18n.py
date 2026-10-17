#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

locales = {
    "zh_TW": {
        "forge.btn_go_inventory": "前往背包"
    },
    "zh_CN": {
        "forge.btn_go_inventory": "前往背包"
    },
    "en": {
        "forge.btn_go_inventory": "Go to Inventory"
    },
    "ja": {
        "forge.btn_go_inventory": "インベントリへ進む"
    },
    "ko": {
        "forge.btn_go_inventory": "인벤토리로 이동"
    },
    "es": {
        "forge.btn_go_inventory": "Ir al Inventario"
    }
}

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../game/data/i18n"))

for loc, kvs in locales.items():
    # 1. <loc>.json
    f1 = os.path.join(base_path, f"{loc}.json")
    if os.path.exists(f1):
        with open(f1, "r", encoding="utf-8") as f:
            d1 = json.load(f)
        d1.update(kvs)
        with open(f1, "w", encoding="utf-8") as f:
            json.dump(d1, f, ensure_ascii=False, indent=2)
            f.write("\n")

    # 2. content/<loc>/ui.json
    f2 = os.path.join(base_path, "content", loc, "ui.json")
    if os.path.exists(f2):
        with open(f2, "r", encoding="utf-8") as f:
            d2 = json.load(f)
        d2.update(kvs)
        with open(f2, "w", encoding="utf-8") as f:
            json.dump(d2, f, ensure_ascii=False, indent=2)
            f.write("\n")

print("Forge inventory shortcut i18n updated successfully!")
