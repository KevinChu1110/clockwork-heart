import json
import os

translations = {
    "已破": {
        "zh_TW": "已破",
        "zh_CN": "已破",
        "en": "Broken",
        "ja": "破壊済",
        "ko": "파괴됨",
        "es": "Roto"
    },
    "[已破]": {
        "zh_TW": "[已破]",
        "zh_CN": "[已破]",
        "en": "[Broken]",
        "ja": "[破壊済]",
        "ko": "[파괴됨]",
        "es": "[Roto]"
    },
    "%s [已破]": {
        "zh_TW": "%s [已破]",
        "zh_CN": "%s [已破]",
        "en": "%s [Broken]",
        "ja": "%s [破壊済]",
        "ko": "%s [파괴됨]",
        "es": "%s [Roto]"
    },
    "battle.part_broken": {
        "zh_TW": "已破",
        "zh_CN": "已破",
        "en": "Broken",
        "ja": "破壊済",
        "ko": "파괴됨",
        "es": "Roto"
    }
}

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
base_dir = "/opt/side/bravesoul-game/game/data/i18n"

for loc in locales:
    # 1. Update content/<loc>/ui.json
    ui_path = os.path.join(base_dir, "content", loc, "ui.json")
    if os.path.exists(ui_path):
        with open(ui_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v_map in translations.items():
            data[k] = v_map[loc]
        sorted_data = {k: data[k] for k in sorted(data.keys())}
        with open(ui_path, "w", encoding="utf-8") as f:
            json.dump(sorted_data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated {ui_path}")

    # 2. Update <loc>.json
    loc_path = os.path.join(base_dir, f"{loc}.json")
    if os.path.exists(loc_path):
        with open(loc_path, "r", encoding="utf-8") as f:
            data_loc = json.load(f)
        for k, v_map in translations.items():
            data_loc[k] = v_map[loc]
        sorted_data_loc = {k: data_loc[k] for k in sorted(data_loc.keys())}
        with open(loc_path, "w", encoding="utf-8") as f:
            json.dump(sorted_data_loc, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated {loc_path}")

print("Translation update complete.")
