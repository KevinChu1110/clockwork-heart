#!/usr/bin/env python3
import json
import os

TRANSLATIONS = {
    "zh_TW": {
        "再次挑戰": "再次挑戰",
        "能量不足，無法再次挑戰關卡！": "能量不足，無法再次挑戰關卡！",
    },
    "zh_CN": {
        "再次挑戰": "再次挑战",
        "能量不足，無法再次挑戰關卡！": "能量不足，无法再次挑战关卡！",
    },
    "en": {
        "再次挑戰": "Retry Stage",
        "能量不足，無法再次挑戰關卡！": "Not enough energy to retry stage!",
    },
    "ja": {
        "再次挑戰": "再挑戦",
        "能量不足，無法再次挑戰關卡！": "エネルギー不足でステージを再挑戦できません！",
    },
    "ko": {
        "再次挑戰": "다시 도전",
        "能量不足，無法再次挑戰關卡！": "에너지가 부족하여 스테이지를 다시 도전할 수 없습니다!",
    },
    "es": {
        "再次挑戰": "Reintentar etapa",
        "能量不足，無法再次挑戰關卡！": "¡Energía insuficiente para reintentar la etapa!",
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
            if k not in data:
                data[k] = v
                added += 1
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"[{loc}] Added {added} keys to {file_path}")

if __name__ == "__main__":
    main()
