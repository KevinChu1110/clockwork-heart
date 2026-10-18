#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

locales = {
    "zh_TW": {
        "title_wall.btn_go_workshop": "前往工坊",
        "title_wall.go_workshop": "前往工坊",
        "前往工坊": "前往工坊"
    },
    "zh_CN": {
        "title_wall.btn_go_workshop": "前往工坊",
        "title_wall.go_workshop": "前往工坊",
        "前往工坊": "前往工坊"
    },
    "en": {
        "title_wall.btn_go_workshop": "Go to Workshop",
        "title_wall.go_workshop": "Go to Workshop",
        "前往工坊": "Go to Workshop"
    },
    "ja": {
        "title_wall.btn_go_workshop": "工房へ進む",
        "title_wall.go_workshop": "工房へ進む",
        "前往工坊": "工房へ進む"
    },
    "ko": {
        "title_wall.btn_go_workshop": "공방으로 이동",
        "title_wall.go_workshop": "공방으로 이동",
        "前往工坊": "공방으로 이동"
    },
    "es": {
        "title_wall.btn_go_workshop": "Ir al Taller",
        "title_wall.go_workshop": "Ir al Taller",
        "前往工坊": "Ir al Taller"
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
