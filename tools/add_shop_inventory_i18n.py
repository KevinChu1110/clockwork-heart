import json
import os

repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
keys = {
    "zh_TW": {
        "shop.btn_go_inventory": "前往背包",
        "前往背包": "前往背包",
    },
    "zh_CN": {
        "shop.btn_go_inventory": "前往背包",
        "前往背包": "前往背包",
    },
    "en": {
        "shop.btn_go_inventory": "Go to Inventory",
        "前往背包": "Go to Inventory",
    },
    "ja": {
        "shop.btn_go_inventory": "インベントリへ進む",
        "前往背包": "インベントリへ進む",
    },
    "ko": {
        "shop.btn_go_inventory": "인벤토리로 이동",
        "前往背包": "인벤토리로 이동",
    },
    "es": {
        "shop.btn_go_inventory": "Ir al Inventario",
        "前往背包": "Ir al Inventario",
    },
}

for loc, kv in keys.items():
    p1 = os.path.join(repo, "game/data/i18n", f"{loc}.json")
    if os.path.exists(p1):
        with open(p1, "r", encoding="utf-8") as f:
            d = json.load(f)
        d.update(kv)
        with open(p1, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("Updated", p1)

    p2 = os.path.join(repo, "game/data/i18n/content", loc, "ui.json")
    if os.path.exists(p2):
        with open(p2, "r", encoding="utf-8") as f:
            d = json.load(f)
        d.update(kv)
        with open(p2, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("Updated", p2)
