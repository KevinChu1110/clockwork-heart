import json
import re

with open("game/data/tables/paperdoll_slots.json") as f:
    spec_data = json.load(f)

spec_names = {}
for slot in spec_data["slots_architecture"]["slots"]:
    for var in slot.get("sample_variants", []):
        spec_names[var["id"]] = var["name"]

print(f"Total spec sample_variants: {len(spec_names)}")

# Now parse paperdoll_select_demo.gd
with open("game/scripts/ui/paperdoll_select_demo.gd") as f:
    gd_text = f.read()

# Check forbidden words
forbidden_pattern = re.compile(r'皮革|天鵝絨|布料|絨毛|棉|leather|velvet')
forbidden_matches = forbidden_pattern.findall(gd_text)
print(f"Forbidden words in paperdoll_select_demo.gd: {forbidden_matches}")

# Extract all variant IDs in RACES_DATA
# Let's extract costume and chassis ids and name_zh
costume_matches = re.findall(r'\{\"id\":\s*\"([^\"]+)\",\s*\"name_zh\":\s*\"([^\"]+)\"', gd_text)
print(f"Found {len(costume_matches)} items in RACES_DATA:")
all_ok = True
id_to_names = {}

for vid, name in costume_matches:
    id_to_names.setdefault(vid, set()).add(name)
    spec_name = spec_names.get(vid, "無外裝 (裸機素體)" if vid == "none" else None)
    match_status = "MATCH" if name == spec_name else "MISMATCH"
    if match_status == "MISMATCH":
        all_ok = False
    print(f"  ID: {vid:<25} | GD name: {name:<15} | Spec name: {str(spec_name):<15} | {match_status}")

# Check weapon default ids
weapons = [
    "wpn_dawn_blade",
    "wpn_knight_lance",
    "wpn_astral_staff",
    "wpn_anvil_greathammer",
    "wpn_spring_claws"
]
print("\nWeapon variants check:")
for wid in weapons:
    sname = spec_names.get(wid)
    print(f"  Weapon: {wid:<25} | Spec name: {sname}")

# Check if any ID maps to multiple names
print("\nMulti-name check:")
for vid, names in id_to_names.items():
    if len(names) > 1:
        print(f"  ERROR: {vid} has multiple names: {names}")
        all_ok = False
    else:
        print(f"  OK: {vid} has single name: {list(names)[0]}")

# Rule 4b-2: Verify all 5 races' item IDs exist in both specs
print("\nCross-spec item ID existence check (Rule 4b-2):")
spec1_path = "game/data/tables/paperdoll_slots.json"
spec2_path = "docs/design/paperdoll_slots.json"
with open(spec1_path) as f:
    text1 = f.read()
with open(spec2_path) as f:
    text2 = f.read()

import os
base_dir = "game/assets/sprites/player/paperdoll"
races = ["rabbit", "lion", "fox", "boar", "macaque"]
missing_ids = []
for race in races:
    race_dir = os.path.join(base_dir, race)
    for root, dirs, files in os.walk(race_dir):
        for file in sorted(files):
            if file.endswith(".png") and not file.startswith("proof_") and not file.startswith("verification_") and not file.startswith("composite_"):
                item_id = file[:-4]
                slot = os.path.basename(root)
                c1 = text1.count(f'"{item_id}"')
                c2 = text2.count(f'"{item_id}"')
                if c1 == 0 or c2 == 0:
                    print(f"  MISSING: {race}/{slot}/{file}: spec1={c1}, spec2={c2}")
                    missing_ids.append((race, slot, file))
                    all_ok = False
                else:
                    print(f"  OK: {race:7} {slot:12} {item_id:25} spec1={c1} spec2={c2}")

if missing_ids:
    print(f"ERROR: {len(missing_ids)} item IDs missing from specs!")
else:
    print("✓ All item IDs across 5 races exist in both spec files!")

if all_ok:
    print("\nALL CHECKS PASSED PERFECTLY!")
else:
    print("\nSOME CHECKS FAILED!")
