#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

locales = {
    "zh_TW": {
        "skill.btn_go_soul_hall": "前往聚魂"
    },
    "zh_CN": {
        "skill.btn_go_soul_hall": "前往聚魂"
    },
    "en": {
        "skill.btn_go_soul_hall": "To Soul Hall"
    },
    "ja": {
        "skill.btn_go_soul_hall": "聚魂殿へ"
    },
    "ko": {
        "skill.btn_go_soul_hall": "집혼전으로"
    },
    "es": {
        "skill.btn_go_soul_hall": "A Salón de Almas"
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

print("SkillDialog soul hall shortcut i18n updated successfully!")
