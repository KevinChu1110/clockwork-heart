#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

locales = {
    "zh_TW": {
        "vault.btn_go_shop": "前往商城"
    },
    "zh_CN": {
        "vault.btn_go_shop": "前往商城"
    },
    "en": {
        "vault.btn_go_shop": "To Shop"
    },
    "ja": {
        "vault.btn_go_shop": "ショップへ"
    },
    "ko": {
        "vault.btn_go_shop": "상점으로"
    },
    "es": {
        "vault.btn_go_shop": "A Tienda"
    }
}

base_path = "/opt/side/bravesoul-game/game/data/i18n"

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

print("ClockworkVault shop shortcut i18n updated successfully!")
