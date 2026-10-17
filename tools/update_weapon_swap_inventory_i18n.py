import json
import os

repo = "/opt/side/bravesoul-game"
content_dir = os.path.join(repo, "game/data/i18n/content")
root_i18n_dir = os.path.join(repo, "game/data/i18n")

trans = {
    "zh_TW": "前往背包",
    "zh_CN": "前往背包",
    "en": "Go to Inventory",
    "ja": "インベントリへ進む",
    "ko": "인벤토리로 이동",
    "es": "Ir al Inventario",
}

keys = [
    "weapon_swap.btn_go_inventory",
    "weapon_swap.go_inventory",
]

# 1. Update content/<loc>/ui.json
for loc, text in trans.items():
    p = os.path.join(content_dir, loc, "ui.json")
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    for k in keys:
        data[k] = text
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"content/{loc}/ui.json updated with keys -> {text}")

# 2. Update <loc>.json
for loc, text in trans.items():
    p = os.path.join(root_i18n_dir, f"{loc}.json")
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    for k in keys:
        data[k] = text
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"{loc}.json updated with keys -> {text}")
