#!/usr/bin/env python3
import json
import os
import sys

repo = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
loc_content = os.path.join(repo, "game/data/i18n/content")
loc_root = os.path.join(repo, "game/data/i18n")

translations = {
    "zh_TW": {
        "✓ 佩戴中": "✓ 佩戴中",
        "佩戴稱號": "佩戴稱號",
        "回到大廳": "回到大廳",
    },
    "zh_CN": {
        "✓ 佩戴中": "✓ 佩戴中",
        "佩戴稱號": "佩戴称号",
        "回到大廳": "回到大厅",
    },
    "en": {
        "✓ 佩戴中": "✓ Equipped",
        "佩戴稱號": "Equip Title",
        "回到大廳": "Back to Lobby",
    },
    "ja": {
        "✓ 佩戴中": "✓ 装備中",
        "佩戴稱號": "称号を装備",
        "回到大廳": "ロビーへ戻る",
    },
    "ko": {
        "✓ 佩戴中": "✓ 착용 중",
        "佩戴稱號": "칭호 착용",
        "回到大廳": "로비로 돌아가기",
    },
    "es": {
        "✓ 佩戴中": "✓ Equipado",
        "佩戴稱號": "Equipar título",
        "回到大廳": "Volver al vestíbulo",
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
