#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

locales = {
    "zh_TW": {
        "skill.btn_go_title_wall": "前往稱號"
    },
    "zh_CN": {
        "skill.btn_go_title_wall": "前往称号"
    },
    "en": {
        "skill.btn_go_title_wall": "Go to Titles"
    },
    "ja": {
        "skill.btn_go_title_wall": "称号一覧へ"
    },
    "ko": {
        "skill.btn_go_title_wall": "칭호로 이동"
    },
    "es": {
        "skill.btn_go_title_wall": "Ir a Títulos"
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

print("SkillDialog title wall shortcut i18n updated successfully!")
