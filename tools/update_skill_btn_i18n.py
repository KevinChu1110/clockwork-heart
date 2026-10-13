#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": "招式 · 核心心法",
    "zh_CN": "招式 · 核心心法",
    "en": "Skills · Core Discipline",
    "ja": "技 · 核心心法",
    "ko": "기술 · 핵심 심법",
    "es": "Habilidades · Disciplina Central"
}

base = "/opt/side/bravesoul-game/game/data/i18n"
key = "招式 · 核心心法"

for loc, trans in locales.items():
    # 1. base/<loc>.json
    p1 = f"{base}/{loc}.json"
    if os.path.exists(p1):
        with open(p1, "r", encoding="utf-8") as f:
            data = json.load(f)
        data[key] = trans
        with open(p1, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated {p1}")

    # 2. base/content/<loc>/ui.json
    p2 = f"{base}/content/{loc}/ui.json"
    if os.path.exists(p2):
        with open(p2, "r", encoding="utf-8") as f:
            data = json.load(f)
        data[key] = trans
        with open(p2, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated {p2}")

print("Done updating i18n files.")
