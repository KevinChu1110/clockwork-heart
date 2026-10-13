#!/usr/bin/env python3
import json
import os

TRANSLATIONS = {
    "zh_TW": {
        "一鍵出售素材": "一鍵出售素材",
        "已鎖定素材已保留未出售": "已鎖定素材已保留未出售",
    },
    "zh_CN": {
        "一鍵出售素材": "一键出售素材",
        "已鎖定素材已保留未出售": "已锁定素材已保留未出售",
    },
    "en": {
        "一鍵出售素材": "Quick-Sell Materials",
        "已鎖定素材已保留未出售": "Locked materials were kept.",
    },
    "ja": {
        "一鍵出售素材": "素材を一括売却",
        "已鎖定素材已保留未出售": "ロックされた素材は保持されました",
    },
    "ko": {
        "一鍵出售素材": "재료 일괄 판매",
        "已鎖定素材已保留未出售": "잠긴 재료는 판매되지 않았습니다",
    },
    "es": {
        "一鍵出售素材": "Vender materiales",
        "已鎖定素材已保留未出售": "Los materiales bloqueados se conservaron.",
    },
}

BASE_DIR = "/opt/side/bravesoul-game/game/data/i18n/content"

def main():
    for loc, entries in TRANSLATIONS.items():
        file_path = os.path.join(BASE_DIR, loc, "ui.json")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        added = 0
        for k, v in entries.items():
            if k not in data or data[k] != v:
                data[k] = v
                added += 1
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"[{loc}] Added/updated {added} keys to {file_path}")

if __name__ == "__main__":
    main()
