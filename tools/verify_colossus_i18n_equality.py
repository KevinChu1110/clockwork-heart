import json
import sys

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
boss_mapping = {
    "colossus_lion": "失控發條獅",
    "colossus_puppet": "霧鐘提線人偶",
    "colossus_elephant": "黑鉚蒸汽巨象"
}

all_ok = True

for loc in locales:
    enemy_file = f"game/data/i18n/content/{loc}/enemy.json"
    ui_file = f"game/data/i18n/content/{loc}/ui.json"
    
    with open(enemy_file, "r", encoding="utf-8") as f:
        enemy_data = json.load(f)
    with open(ui_file, "r", encoding="utf-8") as f:
        ui_data = json.load(f)
        
    for boss_id, zh_tw_key in boss_mapping.items():
        if boss_id not in enemy_data:
            print(f"[FAIL] {loc} {enemy_file} missing {boss_id}")
            all_ok = False
            continue
        enemy_name = enemy_data[boss_id].get("name")
        if zh_tw_key not in ui_data:
            print(f"[FAIL] {loc} {ui_file} missing key '{zh_tw_key}'")
            all_ok = False
            continue
        ui_val = ui_data.get(zh_tw_key)
        if enemy_name != ui_val:
            print(f"[FAIL] {loc} mismatch for {boss_id}/{zh_tw_key}: enemy='{enemy_name}' != ui='{ui_val}'")
            all_ok = False
        else:
            print(f"[OK] {loc}: {boss_id} -> enemy='{enemy_name}' == ui['{zh_tw_key}']='{ui_val}'")

if not all_ok:
    print("VERIFICATION FAILED")
    sys.exit(1)
else:
    print("ALL 6 LOCALES COLOSSUS NAMES EQUAL VERIFIED!")
    sys.exit(0)
