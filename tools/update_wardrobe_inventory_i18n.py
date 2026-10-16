import json
import os

files_and_locales = [
    ("game/data/i18n/content/zh_TW/ui.json", "zh_TW", "前往背包"),
    ("game/data/i18n/content/zh_CN/ui.json", "zh_CN", "前往背包"),
    ("game/data/i18n/content/en/ui.json", "en", "To Bag"),
    ("game/data/i18n/content/ja/ui.json", "ja", "バッグへ"),
    ("game/data/i18n/content/ko/ui.json", "ko", "가방으로"),
    ("game/data/i18n/content/es/ui.json", "es", "A Mochila"),
    ("game/data/i18n/zh_TW.json", "zh_TW", "前往背包"),
    ("game/data/i18n/zh_CN.json", "zh_CN", "前往背包"),
    ("game/data/i18n/en.json", "en", "To Bag"),
    ("game/data/i18n/ja.json", "ja", "バッグへ"),
    ("game/data/i18n/ko.json", "ko", "가방으로"),
    ("game/data/i18n/es.json", "es", "A Mochila"),
]

for filepath, loc, text in files_and_locales:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["wardrobe.btn_go_inventory"] = text
    data["wardrobe.go_inventory"] = text
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Updated {filepath} for {loc} -> {text}")
