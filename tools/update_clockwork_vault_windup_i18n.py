#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

locales = {
    "zh_TW": {
        "vault.btn_go_windup": "前往委託",
    },
    "zh_CN": {
        "vault.btn_go_windup": "前往委托",
    },
    "en": {
        "vault.btn_go_windup": "To Daily",
    },
    "ja": {
        "vault.btn_go_windup": "日課へ",
    },
    "ko": {
        "vault.btn_go_windup": "일일 의뢰로 이동",
    },
    "es": {
        "vault.btn_go_windup": "Ir a Encargos",
    }
}

base_path = "/opt/side/bravesoul-game/game/data/i18n"

for loc, kvs in locales.items():
    # 1. <loc>.json
    f1 = f"{base_path}/{loc}.json"
    with open(f1, "r", encoding="utf-8") as f:
        d1 = json.load(f)
    d1.update(kvs)
    with open(f1, "w", encoding="utf-8") as f:
        json.dump(d1, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # 2. content/<loc>/ui.json
    f2 = f"{base_path}/content/{loc}/ui.json"
    with open(f2, "r", encoding="utf-8") as f:
        d2 = json.load(f)
    d2.update(kvs)
    with open(f2, "w", encoding="utf-8") as f:
        json.dump(d2, f, ensure_ascii=False, indent=2)
        f.write("\n")

print("i18n updated successfully for clockwork_vault windup button!")
