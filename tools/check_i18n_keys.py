import json, os

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
base_dir = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_77530648/game/data/i18n"

keys_to_check = ["核心機芯", "普通", "稀有", "史詩", "傳奇", "彩", "核心碎片"]

for loc in locales:
    p1 = os.path.join(base_dir, f"content/{loc}/ui.json")
    p2 = os.path.join(base_dir, f"{loc}.json")
    d1 = json.load(open(p1, encoding="utf-8")) if os.path.exists(p1) else {}
    d2 = json.load(open(p2, encoding="utf-8")) if os.path.exists(p2) else {}
    print(f"=== {loc} ===")
    for k in keys_to_check:
        print(f"  {k} in content/ui: {k in d1} ({d1.get(k)}), in root: {k in d2} ({d2.get(k)})")
