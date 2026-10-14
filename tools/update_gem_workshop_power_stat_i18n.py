#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

locales = {
    "zh_TW": {
        "gem_workshop.btn_go_power_stat": "前往戰力",
        "前往戰力": "前往戰力"
    },
    "zh_CN": {
        "gem_workshop.btn_go_power_stat": "前往战力",
        "前往戰力": "前往战力"
    },
    "en": {
        "gem_workshop.btn_go_power_stat": "Go to Stats",
        "前往戰力": "Go to Stats"
    },
    "ja": {
        "gem_workshop.btn_go_power_stat": "戦力詳細へ",
        "前往戰力": "戦力詳細へ"
    },
    "ko": {
        "gem_workshop.btn_go_power_stat": "전투력으로 이동",
        "前往戰力": "전투력으로 이동"
    },
    "es": {
        "gem_workshop.btn_go_power_stat": "Ir a Estadísticas",
        "前往戰力": "Ir a Estadísticas"
    }
}

base_path = "game/data/i18n"

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

print("GemWorkshop power stat shortcut i18n updated successfully!")
