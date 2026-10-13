#!/usr/bin/env python3
import json
import os
import sys

repo = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
loc_content = os.path.join(repo, "game/data/i18n/content")
loc_root = os.path.join(repo, "game/data/i18n")

translations = {
    "zh_TW": {
        "卸下稱號": "卸下稱號",
    },
    "zh_CN": {
        "卸下稱號": "卸下称号",
    },
    "en": {
        "卸下稱號": "Unequip Title",
    },
    "ja": {
        "卸下稱號": "称号を外す",
    },
    "ko": {
        "卸下稱號": "칭호 해제",
    },
    "es": {
        "卸下稱號": "Desequipar título",
    }
}

for lang, kv in translations.items():
    p1 = os.path.join(loc_content, lang, "ui.json")
    if os.path.exists(p1):
        with open(p1, "r", encoding="utf-8") as f:
            d1 = json.load(f)
        for k, v in kv.items():
            d1[k] = v
        with open(p1, "w", encoding="utf-8") as f:
            json.dump(d1, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated {p1}")

    p2 = os.path.join(loc_root, f"{lang}.json")
    if os.path.exists(p2):
        with open(p2, "r", encoding="utf-8") as f:
            d2 = json.load(f)
        for k, v in kv.items():
            d2[k] = v
        with open(p2, "w", encoding="utf-8") as f:
            json.dump(d2, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated {p2}")
