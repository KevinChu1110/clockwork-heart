#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

locales = {
    "zh_TW": {
        "inventory.btn_go_wardrobe": "前往衣櫥",
    },
    "zh_CN": {
        "inventory.btn_go_wardrobe": "前往衣橱",
    },
    "en": {
        "inventory.btn_go_wardrobe": "To Wardrobe",
    },
    "ja": {
        "inventory.btn_go_wardrobe": "衣装部屋へ",
    },
    "ko": {
        "inventory.btn_go_wardrobe": "옷장으로",
    },
    "es": {
        "inventory.btn_go_wardrobe": "A Guardarropa",
    }
}

base_path = "game/data/i18n"

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

print("Inventory wardrobe shortcut i18n updated successfully!")
