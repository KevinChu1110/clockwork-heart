#!/usr/bin/env python3
import os
import re

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gd_path = os.path.join(repo_root, "game/scripts/art/paperdoll_renderer.gd")

with open(gd_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update all_races (2 places)
old_all_races = '"kingfisher", "donkey", "scorpion", "mantis"]'
new_all_races = '"kingfisher", "donkey", "scorpion", "mantis", "nightingale"]'
assert content.count(old_all_races) == 2, f"Expected 2 occurrences of old_all_races, found {content.count(old_all_races)}"
content = content.replace(old_all_races, new_all_races)

# 2. Update slots in _get_default_variant_id
slot_replacements = [
    (
        '\t\t\telif race == "mantis":\n\t\t\t\treturn "chassis_mantis_stock"',
        '\t\t\telif race == "mantis":\n\t\t\t\treturn "chassis_mantis_stock"\n\t\t\telif race == "nightingale":\n\t\t\t\treturn "chassis_nightingale_stock"'
    ),
    (
        '\t\t\telif race == "mantis":\n\t\t\t\treturn "head_mantis_canopy_cowl"',
        '\t\t\telif race == "mantis":\n\t\t\t\treturn "head_mantis_canopy_cowl"\n\t\t\telif race == "nightingale":\n\t\t\t\treturn "head_nightingale_dial_cowl"'
    ),
    (
        '\t\t\telif race == "mantis":\n\t\t\t\treturn "key_mantis_vine_brass"',
        '\t\t\telif race == "mantis":\n\t\t\t\treturn "key_mantis_vine_brass"\n\t\t\telif race == "nightingale":\n\t\t\t\treturn "key_nightingale_clef_brass"'
    ),
    (
        '\t\t\telif race == "mantis":\n\t\t\t\treturn "costume_mantis_vine_plate"',
        '\t\t\telif race == "mantis":\n\t\t\t\treturn "costume_mantis_vine_plate"\n\t\t\telif race == "nightingale":\n\t\t\t\treturn "costume_nightingale_chime_plate"'
    ),
    (
        '\t\t\telif race == "mantis":\n\t\t\t\treturn "face_mantis_emerald_goggles"',
        '\t\t\telif race == "mantis":\n\t\t\t\treturn "face_mantis_emerald_goggles"\n\t\t\telif race == "nightingale":\n\t\t\t\treturn "face_nightingale_topaz_goggles"'
    ),
    (
        '\t\t\telif race == "mantis":\n\t\t\t\treturn "weapon_mantis_scythe_claw"',
        '\t\t\telif race == "mantis":\n\t\t\t\treturn "weapon_mantis_scythe_claw"\n\t\t\telif race == "nightingale":\n\t\t\t\treturn "weapon_nightingale_chime_crystal"'
    ),
    (
        '\t\t\telif race == "mantis":\n\t\t\t\treturn "curio_mantis_spring_pack"',
        '\t\t\telif race == "mantis":\n\t\t\t\treturn "curio_mantis_spring_pack"\n\t\t\telif race == "nightingale":\n\t\t\t\treturn "curio_nightingale_chime_tail"'
    ),
]

for old_s, new_s in slot_replacements:
    assert old_s in content, f"Not found: {old_s}"
    content = content.replace(old_s, new_s, 1)

# 3. Update total_races in fallback_spec
assert '"total_races": 70,' in content, "total_races: 70 not found"
content = content.replace('"total_races": 70,', '"total_races": 71,', 1)

# 4. Update races list in fallback_spec
mantis_line = '{"race_id": "mantis", "aliases": ["jade_mantis", "emerald_mantis", "clockwork_mantis", "tinplate_mantis", "scythe_mantis", "canopy_mantis"], "name_zh": "翠刃螳螂", "name_en": "The Jade Mantis", "class_archetype": "武術家 (Monk)"}'
nightingale_line = '{"race_id": "nightingale", "aliases": ["dawn_nightingale", "chime_nightingale", "clockwork_nightingale", "belfry_nightingale", "songbird_nightingale", "golden_nightingale"], "name_zh": "晨音夜鶯", "name_en": "The Dawn Nightingale", "class_archetype": "法師 (Mage)"}'

assert mantis_line in content, "mantis_line not found"
content = content.replace(
    mantis_line,
    mantis_line + ',\n\t\t\t\t' + nightingale_line,
    1
)

with open(gd_path, "w", encoding="utf-8") as f:
    f.write(content)

print("paperdoll_renderer.gd successfully updated for nightingale.")
