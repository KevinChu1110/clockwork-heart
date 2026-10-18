#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

locales = {
    "zh_TW": {
        "title_wall.btn_go_skill": "前往心法",
        "title_wall.go_skill": "前往心法",
        "前往心法": "前往心法"
    },
    "zh_CN": {
        "title_wall.btn_go_skill": "前往心法",
        "title_wall.go_skill": "前往心法",
        "前往心法": "前往心法"
    },
    "en": {
        "title_wall.btn_go_skill": "Go to Skills",
        "title_wall.go_skill": "Go to Skills",
        "前往心法": "Go to Skills"
    },
    "ja": {
        "title_wall.btn_go_skill": "心法へ進む",
        "title_wall.go_skill": "心法へ進む",
        "前往心法": "心法へ進む"
    },
    "ko": {
        "title_wall.btn_go_skill": "심법으로 이동",
        "title_wall.go_skill": "심법으로 이동",
        "前往心法": "심법으로 이동"
    },
    "es": {
        "title_wall.btn_go_skill": "Ir a Habilidades",
        "title_wall.go_skill": "Ir a Habilidades",
        "前往心法": "Ir a Habilidades"
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
