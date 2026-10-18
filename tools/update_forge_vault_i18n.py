#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

locales = {
    "zh_TW": {
        "forge.btn_go_vault": "前往儲能庫",
        "ui.btn_go_vault": "前往儲能庫",
        "前往儲能庫": "前往儲能庫"
    },
    "zh_CN": {
        "forge.btn_go_vault": "前往储能库",
        "ui.btn_go_vault": "前往储能库",
        "前往儲能庫": "前往储能库"
    },
    "en": {
        "forge.btn_go_vault": "To Vault",
        "ui.btn_go_vault": "To Vault",
        "前往儲能庫": "To Vault"
    },
    "ja": {
        "forge.btn_go_vault": "貯蔵庫へ",
        "ui.btn_go_vault": "貯蔵庫へ",
        "前往儲能庫": "貯蔵庫へ"
    },
    "ko": {
        "forge.btn_go_vault": "저장고로 이동",
        "ui.btn_go_vault": "저장고로 이동",
        "前往儲能庫": "저장고로 이동"
    },
    "es": {
        "forge.btn_go_vault": "Ir a Bóveda",
        "ui.btn_go_vault": "Ir a Bóveda",
        "前往儲能庫": "Ir a Bóveda"
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
        print(f"Updated {f1}")

    # 2. content/<loc>/ui.json
    f2 = os.path.join(base_path, "content", loc, "ui.json")
    if os.path.exists(f2):
        with open(f2, "r", encoding="utf-8") as f:
            d2 = json.load(f)
        d2.update(kvs)
        with open(f2, "w", encoding="utf-8") as f:
            json.dump(d2, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated {f2}")
