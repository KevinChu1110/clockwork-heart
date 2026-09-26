#!/usr/bin/env python3
import json

translations = {
    "zh_TW": {
        "下次先破壞%s": "下次先破壞%s",
    },
    "zh_CN": {
        "下次先破壞%s": "下次先破坏%s",
    },
    "en": {
        "下次先破壞%s": "Next time destroy %s first",
    },
    "ja": {
        "下次先破壞%s": "次はまず%sを破壊しよう",
    },
    "ko": {
        "下次先破壞%s": "다음엔 먼저 %s을(를) 파괴하세요",
    },
    "es": {
        "下次先破壞%s": "La próxima vez destruye primero %s",
    }
}

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

for loc in locales:
    kv = translations.get(loc, {})
    # 1. content/<loc>/ui.json
    p1 = f"game/data/i18n/content/{loc}/ui.json"
    try:
        with open(p1, "r", encoding="utf-8") as f:
            d1 = json.load(f)
    except Exception:
        d1 = {}
    for k, v in kv.items():
        d1[k] = v
    with open(p1, "w", encoding="utf-8") as f:
        json.dump(d1, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Updated {p1}")

    # 2. <loc>.json
    p2 = f"game/data/i18n/{loc}.json"
    try:
        with open(p2, "r", encoding="utf-8") as f:
            d2 = json.load(f)
    except Exception:
        d2 = {}
    for k, v in kv.items():
        d2[k] = v
    with open(p2, "w", encoding="utf-8") as f:
        json.dump(d2, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Updated {p2}")

print("Colossus defeat hint i18n sync complete!")
