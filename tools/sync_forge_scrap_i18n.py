#!/usr/bin/env python3
import json
import os

REPO_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_2e0eeb9f/bravesoul-game"

TRANSLATIONS = {
    "zh_TW": {
        "前往拆解": "前往拆解",
        "鐵屑：%d（每次消耗 %d）": "鐵屑：%d（每次消耗 %d）",
    },
    "zh_CN": {
        "前往拆解": "前往拆解",
        "鐵屑：%d（每次消耗 %d）": "铁屑：%d（每次消耗 %d）",
    },
    "en": {
        "前往拆解": "Dismantle",
        "鐵屑：%d（每次消耗 %d）": "Iron Scrap: %d (Cost %d)",
    },
    "ja": {
        "前往拆解": "分解へ",
        "鐵屑：%d（每次消耗 %d）": "鉄くず：%d（消費 %d）",
    },
    "ko": {
        "前往拆解": "분해하러 가기",
        "鐵屑：%d（每次消耗 %d）": "고철: %d (소모 %d)",
    },
    "es": {
        "前往拆解": "Desmontar",
        "鐵屑：%d（每次消耗 %d）": "Chatarra: %d (Coste %d)",
    },
}

for loc, entries in TRANSLATIONS.items():
    # 1. Update content/{loc}/ui.json
    ui_path = os.path.join(REPO_ROOT, f"game/data/i18n/content/{loc}/ui.json")
    if os.path.exists(ui_path):
        with open(ui_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in entries.items():
            data[k] = v
        with open(ui_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Updated {ui_path}")

    # 2. Update root {loc}.json
    root_path = os.path.join(REPO_ROOT, f"game/data/i18n/{loc}.json")
    if os.path.exists(root_path):
        with open(root_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in entries.items():
            data[k] = v
        with open(root_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Updated {root_path}")

print("i18n updated successfully!")
