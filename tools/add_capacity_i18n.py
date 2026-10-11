import json
import os

LOCALES = {
    "zh_TW": {
        "容量 %d/%d": "容量 %d/%d",
        "背包空間已滿": "背包空間已滿",
        "容量": "容量",
    },
    "zh_CN": {
        "容量 %d/%d": "容量 %d/%d",
        "背包空間已滿": "背包空间已满",
        "容量": "容量",
    },
    "en": {
        "容量 %d/%d": "Capacity %d/%d",
        "背包空間已滿": "Backpack is full",
        "容量": "Capacity",
    },
    "ja": {
        "容量 %d/%d": "容量 %d/%d",
        "背包空間已滿": "バッグの空きがありません",
        "容量": "容量",
    },
    "ko": {
        "容量 %d/%d": "용량 %d/%d",
        "背包空間已滿": "가방 공간이 가득 찼습니다",
        "容量": "용량",
    },
    "es": {
        "容量 %d/%d": "Capacidad %d/%d",
        "背包空間已滿": "Espacio de mochila lleno",
        "容量": "Capacidad",
    },
}

base = "/opt/side/bravesoul-game/game/data/i18n"
for loc, entries in LOCALES.items():
    ui_path = os.path.join(base, "content", loc, "ui.json")
    if os.path.exists(ui_path):
        with open(ui_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in entries.items():
            data[k] = v
        with open(ui_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated {ui_path}")

    loc_path = os.path.join(base, f"{loc}.json")
    if os.path.exists(loc_path):
        with open(loc_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in entries.items():
            data[k] = v
        with open(loc_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated {loc_path}")
print("ALL DONE")
