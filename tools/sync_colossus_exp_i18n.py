#!/usr/bin/env python3
import json
import os

new_keys = {
    "zh_TW": {
        "戰鬥經驗": "戰鬥經驗",
        "經驗 +%d": "經驗 +%d",
        "經驗 +0（已達上限）": "經驗 +0（已達上限）",
        "經驗 +0": "經驗 +0",
    },
    "zh_CN": {
        "戰鬥經驗": "战斗经验",
        "經驗 +%d": "经验 +%d",
        "經驗 +0（已達上限）": "经验 +0（已达上限）",
        "經驗 +0": "经验 +0",
    },
    "en": {
        "戰鬥經驗": "Combat EXP",
        "經驗 +%d": "EXP +%d",
        "經驗 +0（已達上限）": "EXP +0 (Max Level)",
        "經驗 +0": "EXP +0",
    },
    "ja": {
        "戰鬥經驗": "戦闘経験値",
        "經驗 +%d": "経験値 +%d",
        "經驗 +0（已達上限）": "経験値 +0（上限到達）",
        "經驗 +0": "経験値 +0",
    },
    "ko": {
        "戰鬥經驗": "전투 경험치",
        "經驗 +%d": "경험치 +%d",
        "經驗 +0（已達上限）": "경험치 +0 (최대 레벨)",
        "經驗 +0": "경험치 +0",
    },
    "es": {
        "戰鬥經驗": "EXP de combate",
        "經驗 +%d": "EXP +%d",
        "經驗 +0（已達上限）": "EXP +0 (Nivel máx.)",
        "經驗 +0": "EXP +0",
    },
}

for lang, entries in new_keys.items():
    # 1. Update content/<lang>/ui.json
    p_content = f"game/data/i18n/content/{lang}/ui.json"
    if os.path.exists(p_content):
        with open(p_content, "r", encoding="utf-8") as f:
            d = json.load(f)
        for k, v in entries.items():
            d[k] = v
        with open(p_content, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated {p_content}")

    # 2. Update <lang>.json
    p_main = f"game/data/i18n/{lang}.json"
    if os.path.exists(p_main):
        with open(p_main, "r", encoding="utf-8") as f:
            d = json.load(f)
        for k, v in entries.items():
            d[k] = v
        with open(p_main, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated {p_main}")
