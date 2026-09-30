#!/usr/bin/env python3
import os
import re

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gd_path = os.path.join(repo_root, "game/scripts/art/paperdoll_renderer.gd")

with open(gd_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update all_races (2 places)
content = content.replace(
    '"kingfisher", "donkey", "scorpion"]',
    '"kingfisher", "donkey", "scorpion", "mantis"]'
)

# 2. Update slots in _get_default_variant_id
slot_replacements = [
    (
        '\t\t\telif race == "scorpion":\n\t\t\t\treturn "chassis_scorpion_stock"',
        '\t\t\telif race == "scorpion":\n\t\t\t\treturn "chassis_scorpion_stock"\n\t\t\telif race == "mantis":\n\t\t\t\treturn "chassis_mantis_stock"'
    ),
    (
        '\t\t\telif race == "scorpion":\n\t\t\t\treturn "head_scorpion_dune_visor"',
        '\t\t\telif race == "scorpion":\n\t\t\t\treturn "head_scorpion_dune_visor"\n\t\t\telif race == "mantis":\n\t\t\t\treturn "head_mantis_canopy_cowl"'
    ),
    (
        '\t\t\telif race == "scorpion":\n\t\t\t\treturn "key_scorpion_cross_brass"',
        '\t\t\telif race == "scorpion":\n\t\t\t\treturn "key_scorpion_cross_brass"\n\t\t\telif race == "mantis":\n\t\t\t\treturn "key_mantis_vine_brass"'
    ),
    (
        '\t\t\telif race == "scorpion":\n\t\t\t\treturn "costume_scorpion_scavenger_plate"',
        '\t\t\telif race == "scorpion":\n\t\t\t\treturn "costume_scorpion_scavenger_plate"\n\t\t\telif race == "mantis":\n\t\t\t\treturn "costume_mantis_vine_plate"'
    ),
    (
        '\t\t\telif race == "scorpion":\n\t\t\t\treturn "face_scorpion_amber_goggles"',
        '\t\t\telif race == "scorpion":\n\t\t\t\treturn "face_scorpion_amber_goggles"\n\t\t\telif race == "mantis":\n\t\t\t\treturn "face_mantis_emerald_goggles"'
    ),
    (
        '\t\t\telif race == "scorpion":\n\t\t\t\treturn "weapon_scorpion_duneshadow_dart"',
        '\t\t\telif race == "scorpion":\n\t\t\t\treturn "weapon_scorpion_duneshadow_dart"\n\t\t\telif race == "mantis":\n\t\t\t\treturn "weapon_mantis_scythe_claw"'
    ),
    (
        '\t\t\telif race == "scorpion":\n\t\t\t\treturn "curio_scorpion_spring_stinger_tail"',
        '\t\t\telif race == "scorpion":\n\t\t\t\treturn "curio_scorpion_spring_stinger_tail"\n\t\t\telif race == "mantis":\n\t\t\t\treturn "curio_mantis_spring_pack"'
    ),
]

for old_s, new_s in slot_replacements:
    assert old_s in content, f"Not found: {old_s}"
    content = content.replace(old_s, new_s, 1)

# 3. Update total_races in fallback_spec
assert '"total_races": 69,' in content, "total_races: 69 not found"
content = content.replace('"total_races": 69,', '"total_races": 70,', 1)

# 4. Update races list in fallback_spec
scorpion_line = '{"race_id": "scorpion", "aliases": ["duneshadow_scorpion", "sand_scorpion", "clockwork_scorpion", "tinplate_scorpion", "stinger_scorpion", "junkyard_scorpion"], "name_zh": "伏影沙蠍", "name_en": "The Duneshadow Scorpion", "class_archetype": "忍者 (Ninja)"}'
mantis_line = '{"race_id": "mantis", "aliases": ["jade_mantis", "emerald_mantis", "clockwork_mantis", "tinplate_mantis", "scythe_mantis", "canopy_mantis"], "name_zh": "翠刃螳螂", "name_en": "The Jade Mantis", "class_archetype": "武術家 (Monk)"}'

assert scorpion_line in content, "scorpion_line not found"
content = content.replace(
    scorpion_line,
    scorpion_line + ',\n\t\t\t\t' + mantis_line,
    1
)

with open(gd_path, "w", encoding="utf-8") as f:
    f.write(content)

print("paperdoll_renderer.gd successfully updated for mantis.")
