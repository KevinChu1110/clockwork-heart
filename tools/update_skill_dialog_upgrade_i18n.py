#!/usr/bin/env python3
import json
import os

translations = {
    "突破升階": {
        "zh_TW": "突破升階",
        "zh_CN": "突破升阶",
        "en": "Breakthrough",
        "ja": "突破昇階",
        "ko": "돌파 승급",
        "es": "Avance de rango"
    },
    "體悟習得": {
        "zh_TW": "體悟習得",
        "zh_CN": "体悟习得",
        "en": "Comprehend",
        "ja": "体悟習得",
        "ko": "깨달음 습득",
        "es": "Comprender y aprender"
    },
    "Lv.MAX · 極階": {
        "zh_TW": "Lv.MAX · 極階",
        "zh_CN": "Lv.MAX · 极阶",
        "en": "Lv.MAX · Mastered",
        "ja": "Lv.MAX · 極階",
        "ko": "Lv.MAX · 극계",
        "es": "Nv.MAX · Maestro"
    }
}

base_dir = "/opt/side/bravesoul-game/game/data/i18n"
locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

for key, loc_map in translations.items():
    for loc in locales:
        trans = loc_map[loc]
        # 1. root /loc.json
        p1 = f"{base_dir}/{loc}.json"
        if os.path.exists(p1):
            with open(p1, "r", encoding="utf-8") as f:
                d1 = json.load(f)
            d1[key] = trans
            with open(p1, "w", encoding="utf-8") as f:
                json.dump(d1, f, ensure_ascii=False, indent=2)
                f.write("\n")
            print(f"Updated {p1} with '{key}': '{trans}'")

        # 2. content/<loc>/ui.json
        p2 = f"{base_dir}/content/{loc}/ui.json"
        if os.path.exists(p2):
            with open(p2, "r", encoding="utf-8") as f:
                d2 = json.load(f)
            d2[key] = trans
            with open(p2, "w", encoding="utf-8") as f:
                json.dump(d2, f, ensure_ascii=False, indent=2)
                f.write("\n")
            print(f"Updated {p2} with '{key}': '{trans}'")

print("Done updating i18n entries.")
