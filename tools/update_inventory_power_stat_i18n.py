import json
import os

entries = {
    "zh_TW": {
        "inventory.btn_go_power_stat": "前往戰力",
        "power_stat.btn_go_inventory": "前往背包",
    },
    "zh_CN": {
        "inventory.btn_go_power_stat": "前往战力",
        "power_stat.btn_go_inventory": "前往背包",
    },
    "en": {
        "inventory.btn_go_power_stat": "Go to Stats",
        "power_stat.btn_go_inventory": "Go to Inventory",
    },
    "ja": {
        "inventory.btn_go_power_stat": "戦力詳細へ",
        "power_stat.btn_go_inventory": "インベントリへ進む",
    },
    "ko": {
        "inventory.btn_go_power_stat": "전투력으로 이동",
        "power_stat.btn_go_inventory": "인벤토리로 이동",
    },
    "es": {
        "inventory.btn_go_power_stat": "Ir a Estadísticas",
        "power_stat.btn_go_inventory": "Ir al Inventario",
    }
}

base_dir = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_2d1c7fbd/bravesoul-game"

# 1. 更新 game/data/i18n/{locale}.json
for loc, kv in entries.items():
    p = os.path.join(base_dir, f"game/data/i18n/{loc}.json")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.update(kv)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated {p}")

# 2. 更新 game/data/i18n/content/{locale}/ui.json
for loc, kv in entries.items():
    p = os.path.join(base_dir, f"game/data/i18n/content/{loc}/ui.json")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.update(kv)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated {p}")

print("All i18n updated successfully in worktree!")
