import json
import os

translations = {
    "zh_TW": ("前往衣櫥", "前往衣櫥"),
    "zh_CN": ("前往衣橱", "前往衣橱"),
    "en": ("To Wardrobe", "To Wardrobe"),
    "ja": ("衣装部屋へ", "衣装部屋へ"),
    "ko": ("의상실로", "의상실로"),
    "es": ("Al Armario", "Al Armario")
}

files = [
    ("zh_TW", "game/data/i18n/zh_TW.json"),
    ("zh_CN", "game/data/i18n/zh_CN.json"),
    ("en", "game/data/i18n/en.json"),
    ("ja", "game/data/i18n/ja.json"),
    ("ko", "game/data/i18n/ko.json"),
    ("es", "game/data/i18n/es.json"),
    ("zh_TW", "game/data/i18n/content/zh_TW/ui.json"),
    ("zh_CN", "game/data/i18n/content/zh_CN/ui.json"),
    ("en", "game/data/i18n/content/en/ui.json"),
    ("ja", "game/data/i18n/content/ja/ui.json"),
    ("ko", "game/data/i18n/content/ko/ui.json"),
    ("es", "game/data/i18n/content/es/ui.json"),
]

for lang, filepath in files:
    full_path = os.path.join("/opt/side/bravesoul-game", filepath)
    with open(full_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    go_val, btn_val = translations[lang]
    data["vault.go_wardrobe"] = go_val
    data["vault.btn_go_wardrobe"] = btn_val
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Updated {filepath} with {lang} translations: {go_val}")
