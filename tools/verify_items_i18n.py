import json, os, re

ROOT = "/opt/side/bravesoul-game"
LOCALES = ["zh_CN", "en", "ja", "ko", "es"]

cat_path = f"{ROOT}/game/scripts/systems/inventory_system.gd"
with open(cat_path, 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'^\t"(\w+)":\s*\{', text, re.MULTILINE)
print("CATALOG items in GDScript:", len(matches), matches)

for loc in LOCALES:
    p = f"{ROOT}/game/data/i18n/content/{loc}/item.json"
    if not os.path.exists(p):
        print(f"Missing {p}")
        continue
    with open(p, 'r', encoding='utf-8') as f:
        data = json.load(f)
    missing = [m for m in matches if m not in data]
    print(f"[{loc}] count: {len(data)}, missing: {missing}")
