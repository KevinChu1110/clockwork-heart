#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from pathlib import Path

locales = {
    "zh_TW": "前往儲能庫",
    "zh_CN": "前往储能库",
    "en": "To Vault",
    "ja": "貯蔵庫へ",
    "ko": "저장고로 이동",
    "es": "Ir a Bóveda"
}

base_dir = Path("/opt/side/bravesoul-game/game/data/i18n")

for loc, text in locales.items():
    # 1. game/data/i18n/{loc}.json
    p1 = base_dir / f"{loc}.json"
    if p1.exists():
        with open(p1, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["gem_workshop.btn_go_vault"] = text
        data["ui.btn_go_vault"] = text
        data["前往儲能庫"] = text
        with open(p1, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")

    # 2. game/data/i18n/content/{loc}/ui.json
    p2 = base_dir / "content" / loc / "ui.json"
    if p2.exists():
        with open(p2, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["gem_workshop.btn_go_vault"] = text
        data["ui.btn_go_vault"] = text
        data["前往儲能庫"] = text
        with open(p2, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")

print("All i18n files updated successfully with gem_workshop.btn_go_vault, ui.btn_go_vault, and 前往儲能庫.")
