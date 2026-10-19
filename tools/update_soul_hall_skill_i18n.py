#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

locales = {
    "zh_TW": {
        "soul_hall.btn_go_skill": "前往心法",
        "soul_hall.go_skill": "前往心法"
    },
    "zh_CN": {
        "soul_hall.btn_go_skill": "前往心法",
        "soul_hall.go_skill": "前往心法"
    },
    "en": {
        "soul_hall.btn_go_skill": "To Skills",
        "soul_hall.go_skill": "To Skills"
    },
    "ja": {
        "soul_hall.btn_go_skill": "心法へ",
        "soul_hall.go_skill": "心法へ"
    },
    "ko": {
        "soul_hall.btn_go_skill": "심법으로",
        "soul_hall.go_skill": "심법으로"
    },
    "es": {
        "soul_hall.btn_go_skill": "A Habilidades",
        "soul_hall.go_skill": "A Habilidades"
    }
}

base_path = "/opt/side/bravesoul-game/game/data/i18n"

for loc, kvs in locales.items():
    f1 = f"{base_path}/{loc}.json"
    if os.path.exists(f1):
        with open(f1, "r", encoding="utf-8") as f:
            d1 = json.load(f)
        d1.update(kvs)
        with open(f1, "w", encoding="utf-8") as f:
            json.dump(d1, f, ensure_ascii=False, indent=2)
            f.write("\n")

    f2 = f"{base_path}/content/{loc}/ui.json"
    if os.path.exists(f2):
        with open(f2, "r", encoding="utf-8") as f:
            d2 = json.load(f)
        d2.update(kvs)
        with open(f2, "w", encoding="utf-8") as f:
            json.dump(d2, f, ensure_ascii=False, indent=2)
            f.write("\n")

print("Soul hall skill shortcut i18n updated successfully!")
