import json

translations = {
    "zh_TW": "傷害貢獻",
    "zh_CN": "伤害贡献",
    "en": "Damage Contribution",
    "ja": "ダメージ貢献",
    "ko": "피해 기여",
    "es": "Contribución de daño",
}

for lang, val in translations.items():
    # 1. ui.json
    ui_path = f"game/data/i18n/content/{lang}/ui.json"
    with open(ui_path, "r", encoding="utf-8") as f:
        d = json.load(f)
    d["傷害貢獻"] = val
    with open(ui_path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"Updated {ui_path} with 傷害貢獻 -> {val}")

    # 2. root json
    root_path = f"game/data/i18n/{lang}.json"
    with open(root_path, "r", encoding="utf-8") as f:
        d2 = json.load(f)
    d2["傷害貢獻"] = val
    with open(root_path, "w", encoding="utf-8") as f:
        json.dump(d2, f, ensure_ascii=False, indent=2)
    print(f"Updated {root_path} with 傷害貢獻 -> {val}")
