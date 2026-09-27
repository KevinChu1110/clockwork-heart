import json
import os

with open("game/data/tables/equipment.json", "r", encoding="utf-8") as f:
    eq_data = json.load(f)

bases = eq_data.get("bases", {})

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

for loc in locales:
    p_ui = f"game/data/i18n/content/{loc}/ui.json"
    p_wpn = f"game/data/i18n/content/{loc}/weapon.json"
    p_root = f"game/data/i18n/{loc}.json"
    
    ui_data = {}
    wpn_data = {}
    root_data = {}
    if os.path.exists(p_ui):
        with open(p_ui, "r", encoding="utf-8") as f:
            ui_data = json.load(f)
    if os.path.exists(p_wpn):
        with open(p_wpn, "r", encoding="utf-8") as f:
            wpn_data = json.load(f)
    if os.path.exists(p_root):
        with open(p_root, "r", encoding="utf-8") as f:
            root_data = json.load(f)
            
    found_count = 0
    missing = []
    for bid, binfo in bases.items():
        name = binfo.get("name", "")
        # Check if name is in wpn_data or ui_data or root_data
        in_wpn = name in wpn_data
        in_ui = name in ui_data
        in_root = name in root_data
        if in_wpn or in_ui or in_root:
            found_count += 1
        else:
            missing.append(f"{bid}({name})")
    print(f"[{loc}] Translated: {found_count}/{len(bases)}, Missing: {len(missing)}")
    if missing:
        print(f"  Missing sample: {missing[:5]}")
