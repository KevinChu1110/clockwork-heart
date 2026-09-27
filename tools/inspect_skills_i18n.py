import json
import os

root = "/opt/side/bravesoul-game"
locales = ["zh_CN", "en", "ja", "ko", "es"]
fields = ["name", "desc", "lv2", "lv3", "unlock_hint"]

for loc in locales:
    p = f"{root}/game/data/i18n/content/{loc}/skill.json"
    data = json.load(open(p, encoding="utf-8"))
    print(f"=== {loc} (total {len(data)}) ===")
    sample_ids = ["slash", "counter_strike", "emergency_heal", "thunder_fury"]
    for sid in sample_ids:
        entry = data.get(sid, {})
        print(f"  {sid}: name='{entry.get('name')}', desc='{entry.get('desc')[:30]}...', lv2='{entry.get('lv2')}', unlock='{entry.get('unlock_hint')}'")
