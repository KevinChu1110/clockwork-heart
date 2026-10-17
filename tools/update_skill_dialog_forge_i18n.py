#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

locales = {
    "zh_TW": {
        "skill.btn_go_forge": "前往鍛造",
        "ui.btn_go_forge": "前往鍛造",
        "前往鍛造": "前往鍛造"
    },
    "zh_CN": {
        "skill.btn_go_forge": "前往锻造",
        "ui.btn_go_forge": "前往锻造",
        "前往鍛造": "前往锻造"
    },
    "en": {
        "skill.btn_go_forge": "Go to Forge",
        "ui.btn_go_forge": "Go to Forge",
        "前往鍛造": "Go to Forge"
    },
    "ja": {
        "skill.btn_go_forge": "鍛造へ進む",
        "ui.btn_go_forge": "鍛造へ進む",
        "前往鍛造": "鍛造へ進む"
    },
    "ko": {
        "skill.btn_go_forge": "단조로 이동",
        "ui.btn_go_forge": "단조로 이동",
        "前往鍛造": "단조로 이동"
    },
    "es": {
        "skill.btn_go_forge": "Ir a Forja",
        "ui.btn_go_forge": "Ir a Forja",
        "前往鍛造": "Ir a Forja"
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

print("Skill dialog forge shortcut i18n updated successfully!")
