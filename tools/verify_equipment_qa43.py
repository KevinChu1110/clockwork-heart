import json
import os

ROOT = "/opt/side/bravesoul-game"
eq_path = os.path.join(ROOT, "game/data/tables/equipment.json")
with open(eq_path, "r", encoding="utf-8") as f:
    eq_data = json.load(f)

bases = eq_data.get("bases", {})
print(f"Total bases in equipment.json: {len(bases)}")

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
dicts = {}
for loc in locales:
    p = os.path.join(ROOT, f"game/data/i18n/content/{loc}/weapon.json")
    with open(p, "r", encoding="utf-8") as f:
        dicts[loc] = json.load(f)

missing = []
for base_id, info in bases.items():
    name = info.get("name", "")
    slot = info.get("slot", "")
    tier = info.get("tier", 1)
    trans = {}
    for loc in locales:
        t = dicts[loc].get(name) or dicts[loc].get(base_id)
        if not t:
            missing.append((loc, base_id, name))
        trans[loc] = t or "MISSING"

print(f"Missing count: {len(missing)}")
if missing:
    for m in missing:
        print(f"MISSING: {m}")
else:
    print("ALL 44 BASES HAVE COMPLETE 6-LOCALE TRANSLATIONS!")

# Check special keys: 銹劍, 鏽劍, 微末之刃, 空手
specials = ["銹劍", "鏽劍", "微末之刃", "空手"]
for s in specials:
    print(f"\nSpecial key [{s}]:")
    for loc in locales:
        print(f"  {loc}: {dicts[loc].get(s)}")
