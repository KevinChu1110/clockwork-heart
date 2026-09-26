#!/usr/bin/env python3
"""更新新手引導觸控化與多語系詞條。
將觸控底列提示加入六語系 content/<lang>/ui.json 與外層 <lang>.json。
"""
import json
import os

BASE_DIR = "/opt/side/bravesoul-game/game/data/i18n"
LOCALES = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

TRANSLATIONS = {
    "zh_TW": {
        "點一下繼續 · 部分步驟可「稍後再說」": "點一下繼續 · 部分步驟可「稍後再說」",
        "點下一步 · 部分步驟可「稍後再說」": "點下一步 · 部分步驟可「稍後再說」",
        "點一下繼續": "點一下繼續",
        "點下一步": "點下一步",
    },
    "zh_CN": {
        "點一下繼續 · 部分步驟可「稍後再說」": "点一下继续 · 部分步骤可「稍后再说」",
        "點下一步 · 部分步驟可「稍後再說」": "点下一步 · 部分步骤可「稍后再说」",
        "點一下繼續": "点一下继续",
        "點下一步": "点下一步",
    },
    "en": {
        "點一下繼續 · 部分步驟可「稍後再說」": 'Tap to continue · Some steps can be skipped with "Later"',
        "點下一步 · 部分步驟可「稍後再說」": 'Tap Next · Some steps can be skipped with "Later"',
        "點一下繼續": "Tap to continue",
        "點下一步": "Tap Next",
    },
    "ja": {
        "點一下繼續 · 部分步驟可「稍後再說」": "タップで進む · 一部の手順は「あとで」でスキップ可能",
        "點下一步 · 部分步驟可「稍後再說」": "「次へ」をタップ · 一部の手順は「あとで」でスキップ可能",
        "點一下繼續": "タップで進む",
        "點下一步": "「次へ」をタップ",
    },
    "ko": {
        "點一下繼續 · 部分步驟可「稍後再說」": "탭하여 계속 · 일부 단계는 「나중에」로 건너뛰기 가능",
        "點下一步 · 部分步驟可「稍後再說」": "「다음」 탭 · 일부 단계는 「나중에」로 건너뛰기 가능",
        "點一下繼續": "탭하여 계속",
        "點下一步": "「다음」 탭",
    },
    "es": {
        "點一下繼續 · 部分步驟可「稍後再說」": "Toca para continuar · Algunos pasos se pueden omitir con «Más tarde»",
        "點下一步 · 部分步驟可「稍後再說」": "Toca Siguiente · Algunos pasos se pueden omitir con «Más tarde»",
        "點一下繼續": "Toca para continuar",
        "點下一步": "Toca Siguiente",
    },
}

def update_file(filepath, entries):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    changed = False
    for k, v in entries.items():
        if data.get(k) != v:
            data[k] = v
            changed = True
    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated: {filepath}")
    else:
        print(f"No changes: {filepath}")

def main():
    for loc in LOCALES:
        content_ui = os.path.join(BASE_DIR, "content", loc, "ui.json")
        outer_json = os.path.join(BASE_DIR, f"{loc}.json")
        update_file(content_ui, TRANSLATIONS[loc])
        update_file(outer_json, TRANSLATIONS[loc])

if __name__ == "__main__":
    main()
