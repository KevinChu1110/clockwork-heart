import json
import os

TRANSLATIONS = {
    "zh_TW": {
        "部位破壞": "部位破壞",
        "鐵屑 +%d": "鐵屑 +%d",
    },
    "zh_CN": {
        "部位破壞": "部位破坏",
        "鐵屑 +%d": "铁屑 +%d",
    },
    "en": {
        "部位破壞": "Part Break",
        "鐵屑 +%d": "Scrap Iron +%d",
    },
    "ja": {
        "部位破壞": "部位破壊",
        "鐵屑 +%d": "鉄屑 +%d",
    },
    "ko": {
        "部位破壞": "부위 파괴",
        "鐵屑 +%d": "철 부스러기 +%d",
    },
    "es": {
        "部位破壞": "Parte destruida",
        "鐵屑 +%d": "Chatarra +%d",
    },
}

def sync_locales():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    content_dir = os.path.join(base_dir, "game", "data", "i18n", "content")
    root_i18n_dir = os.path.join(base_dir, "game", "data", "i18n")

    for loc, trans in TRANSLATIONS.items():
        # 1. Update content/<loc>/ui.json
        ui_path = os.path.join(content_dir, loc, "ui.json")
        if os.path.exists(ui_path):
            with open(ui_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k, v in trans.items():
                data[k] = v
            with open(ui_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[OK] Updated {ui_path}")
        else:
            print(f"[WARN] Not found: {ui_path}")

        # 2. Update root <loc>.json
        root_path = os.path.join(root_i18n_dir, f"{loc}.json")
        if os.path.exists(root_path):
            with open(root_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k, v in trans.items():
                data[k] = v
            with open(root_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[OK] Updated {root_path}")
        else:
            print(f"[WARN] Not found: {root_path}")

if __name__ == "__main__":
    sync_locales()
