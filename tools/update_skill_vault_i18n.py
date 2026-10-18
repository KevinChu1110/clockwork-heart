#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

locales = {
    "zh_TW": {
        "skill.btn_go_vault": "前往儲能庫"
    },
    "zh_CN": {
        "skill.btn_go_vault": "前往储能库"
    },
    "en": {
        "skill.btn_go_vault": "To Vault"
    },
    "ja": {
        "skill.btn_go_vault": "貯蔵庫へ"
    },
    "ko": {
        "skill.btn_go_vault": "저장고로 이동"
    },
    "es": {
        "skill.btn_go_vault": "Ir a Bóveda"
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

print("SkillDialog vault shortcut i18n updated successfully!")
