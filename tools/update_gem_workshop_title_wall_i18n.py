#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

locales = {
    "zh_TW": {
        "gem_workshop.btn_go_title_wall": "前往稱號",
        "gem_workshop.go_title_wall": "前往稱號",
        "ui.btn_go_title_wall": "前往稱號",
        "前往稱號": "前往稱號"
    },
    "zh_CN": {
        "gem_workshop.btn_go_title_wall": "前往称号",
        "gem_workshop.go_title_wall": "前往称号",
        "ui.btn_go_title_wall": "前往称号",
        "前往稱號": "前往称号"
    },
    "en": {
        "gem_workshop.btn_go_title_wall": "To Titles",
        "gem_workshop.go_title_wall": "To Titles",
        "ui.btn_go_title_wall": "To Titles",
        "前往稱號": "To Titles"
    },
    "ja": {
        "gem_workshop.btn_go_title_wall": "称号へ",
        "gem_workshop.go_title_wall": "称号へ",
        "ui.btn_go_title_wall": "称号へ",
        "前往稱號": "称号へ"
    },
    "ko": {
        "gem_workshop.btn_go_title_wall": "칭호로 이동",
        "gem_workshop.go_title_wall": "칭호로 이동",
        "ui.btn_go_title_wall": "칭호로 이동",
        "前往稱號": "칭호로 이동"
    },
    "es": {
        "gem_workshop.btn_go_title_wall": "Ir a Títulos",
        "gem_workshop.go_title_wall": "Ir a Títulos",
        "ui.btn_go_title_wall": "Ir a Títulos",
        "前往稱號": "Ir a Títulos"
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
