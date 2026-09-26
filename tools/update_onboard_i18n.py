#!/usr/bin/env python3
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# 六語系字典定義
TRANSLATIONS = {
    "zh_TW": {
        "下一步": "下一步",
        "稍後再說": "稍後再說",
        "新手完成": "新手完成",
        "新手引導 · 第 %d／%d 步": "新手引導 · 第 %d／%d 步",
        "第 %d／%d 步": "第 %d／%d 步",
        "空白鍵／下一步 · 部分步驟可「稍後再說」": "空白鍵／下一步 · 部分步驟可「稍後再說」",
        "封靈": "封靈",
    },
    "zh_CN": {
        "下一步": "下一步",
        "稍後再說": "稍后再说",
        "新手完成": "新手完成",
        "新手引導 · 第 %d／%d 步": "新手引导 · 第 %d／%d 步",
        "第 %d／%d 步": "第 %d／%d 步",
        "空白鍵／下一步 · 部分步驟可「稍後再說」": "空格键／下一步 · 部分步骤可「稍后再说」",
        "封靈": "封灵",
    },
    "en": {
        "下一步": "Next",
        "稍後再說": "Later",
        "新手完成": "Tutorial Complete",
        "新手引導 · 第 %d／%d 步": "Tutorial · Step %d/%d",
        "第 %d／%d 步": "Step %d/%d",
        "空白鍵／下一步 · 部分步驟可「稍後再說」": 'Space / Next · Some steps can be skipped with "Later"',
        "封靈": "Soul Seal",
    },
    "ja": {
        "下一步": "次へ",
        "稍後再說": "あとで",
        "新手完成": "チュートリアル完了",
        "新手引導 · 第 %d／%d 步": "チュートリアル · ステップ %d/%d",
        "第 %d／%d 步": "ステップ %d/%d",
        "空白鍵／下一步 · 部分步驟可「稍後再說」": "スペース / 次へ · 一部の手順は「あとで」でスキップ可能",
        "封靈": "封霊",
    },
    "ko": {
        "下一步": "다음",
        "稍後再說": "나중에",
        "新手完成": "튜토리얼 완료",
        "新手引導 · 第 %d／%d 步": "튜토리얼 · %d/%d 단계",
        "第 %d／%d 步": "%d/%d 단계",
        "空白鍵／下一步 · 部分步驟可「稍後再說」": "스페이스바 / 다음 · 일부 단계는 「나중에」로 건너뛰기 가능",
        "封靈": "봉령",
    },
    "es": {
        "下一步": "Siguiente",
        "稍後再說": "Más tarde",
        "新手完成": "Tutorial completado",
        "新手引導 · 第 %d／%d 步": "Tutorial · Paso %d/%d",
        "第 %d／%d 步": "Paso %d/%d",
        "空白鍵／下一步 · 部分步驟可「稍後再說」": "Espacio / Siguiente · Algunos pasos se pueden omitir con «Más tarde»",
        "封靈": "Sello de alma",
    },
}

def update_json_file(file_path: Path, new_entries: dict):
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    added = 0
    for k, v in new_entries.items():
        if k not in data or data[k] != v:
            data[k] = v
            added += 1

    # 排序並寫回
    sorted_data = dict(sorted(data.items(), key=lambda x: x[0]))
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Updated {file_path.relative_to(REPO_ROOT)}: {added} entries added/updated")

def main():
    for loc, entries in TRANSLATIONS.items():
        # 1. 更新 data/i18n/content/<loc>/ui.json
        ui_json = REPO_ROOT / "game" / "data" / "i18n" / "content" / loc / "ui.json"
        update_json_file(ui_json, entries)

        # 2. 更新 data/i18n/<loc>.json
        loc_json = REPO_ROOT / "game" / "data" / "i18n" / f"{loc}.json"
        update_json_file(loc_json, entries)

if __name__ == "__main__":
    main()
