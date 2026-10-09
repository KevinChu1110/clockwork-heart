#!/usr/bin/env python3
import json
import os

TRANSLATIONS = {
    "zh_TW": {
        "防禦": "防禦",
        "生命": "生命",
        "暴傷": "暴傷",
        "暴擊傷害": "暴擊傷害",
    },
    "zh_CN": {
        "防禦": "防御",
        "生命": "生命",
        "暴傷": "暴伤",
        "暴擊傷害": "暴击伤害",
    },
    "en": {
        "防禦": "DEF",
        "生命": "HP",
        "暴傷": "Crit DMG",
        "暴擊傷害": "Critical Damage",
    },
    "ja": {
        "防禦": "防御",
        "生命": "HP",
        "暴傷": "会心ダメ",
        "暴擊傷害": "会心ダメージ",
    },
    "ko": {
        "防禦": "방어",
        "生命": "HP",
        "暴傷": "치명타 피해",
        "暴擊傷害": "치명타 대미지",
    },
    "es": {
        "防禦": "DEF",
        "生命": "Salud",
        "暴傷": "Daño Crít.",
        "暴擊傷害": "Daño Crítico",
    },
}

BASE_DIR = "/opt/side/bravesoul-game/game/data/i18n/content"

for lc, kv in TRANSLATIONS.items():
    path = os.path.join(BASE_DIR, lc, "ui.json")
    if not os.path.exists(path):
        print(f"Skipping missing {path}")
        continue
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    changed = False
    for k, v in kv.items():
        if k not in data or data[k] != v:
            data[k] = v
            changed = True
    if changed:
        # Keep keys sorted for deterministic diff
        sorted_data = dict(sorted(data.items(), key=lambda x: x[0]))
        with open(path, "w", encoding="utf-8") as f:
            json.dump(sorted_data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated {lc}/ui.json with substat terms")
    else:
        print(f"No changes needed for {lc}/ui.json")
