#!/usr/bin/env python3
import os
import re

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gd_path = os.path.join(repo_root, "game/scripts/art/paperdoll_renderer.gd")

with open(gd_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update all_races (2 places)
content = content.replace(
    '"kingfisher", "donkey"]',
    '"kingfisher", "donkey", "scorpion"]'
)

# 2. Update slots in _get_default_variant_id
slot_replacements = [
    (
        '\t\t\telif race == "donkey":\n\t\t\t\treturn "chassis_donkey_tinplate_default"',
        '\t\t\telif race == "donkey":\n\t\t\t\treturn "chassis_donkey_tinplate_default"\n\t\t\telif race == "scorpion":\n\t\t\t\treturn "chassis_scorpion_stock"'
    ),
    (
        '\t\t\telif race == "donkey":\n\t\t\t\treturn "head_donkey_ratchet_ears_cowl"',
        '\t\t\telif race == "donkey":\n\t\t\t\treturn "head_donkey_ratchet_ears_cowl"\n\t\t\telif race == "scorpion":\n\t\t\t\treturn "head_scorpion_dune_visor"'
    ),
    (
        '\t\t\telif race == "donkey":\n\t\t\t\treturn "key_donkey_dawn_clover_brass"',
        '\t\t\telif race == "donkey":\n\t\t\t\treturn "key_donkey_dawn_clover_brass"\n\t\t\telif race == "scorpion":\n\t\t\t\treturn "key_scorpion_cross_brass"'
    ),
    (
        '\t\t\telif race == "donkey":\n\t\t\t\treturn "costume_donkey_sapper_harness"',
        '\t\t\telif race == "donkey":\n\t\t\t\treturn "costume_donkey_sapper_harness"\n\t\t\telif race == "scorpion":\n\t\t\t\treturn "costume_scorpion_scavenger_plate"'
    ),
    (
        '\t\t\telif race == "donkey":\n\t\t\t\treturn "face_donkey_slate_goggles"',
        '\t\t\telif race == "donkey":\n\t\t\t\treturn "face_donkey_slate_goggles"\n\t\t\telif race == "scorpion":\n\t\t\t\treturn "face_scorpion_amber_goggles"'
    ),
    (
        '\t\t\telif race == "donkey":\n\t\t\t\treturn "weapon_donkey_bazaar_clearing_axe"',
        '\t\t\telif race == "donkey":\n\t\t\t\treturn "weapon_donkey_bazaar_clearing_axe"\n\t\t\telif race == "scorpion":\n\t\t\t\treturn "weapon_scorpion_duneshadow_dart"'
    ),
    (
        '\t\t\telif race == "donkey":\n\t\t\t\treturn "curio_donkey_cograil_pack_tail"',
        '\t\t\telif race == "donkey":\n\t\t\t\treturn "curio_donkey_cograil_pack_tail"\n\t\t\telif race == "scorpion":\n\t\t\t\treturn "curio_scorpion_spring_stinger_tail"'
    ),
]

for old_s, new_s in slot_replacements:
    assert old_s in content, f"Not found: {old_s}"
    content = content.replace(old_s, new_s, 1)

# 3. Update total_races in fallback_spec
assert '"total_races": 68,' in content, "total_races: 68 not found"
content = content.replace('"total_races": 68,', '"total_races": 69,', 1)

# 4. Update races list in fallback_spec
donkey_line = '{"race_id": "donkey", "aliases": ["sapper_donkey", "bazaar_donkey", "clockwork_donkey", "burro", "pack_donkey", "iron_donkey"], "name_zh": "闢道頑驢", "name_en": "The Sapper Donkey", "class_archetype": "戰士 (Viking)"}'
scorpion_line = '{"race_id": "scorpion", "aliases": ["duneshadow_scorpion", "sand_scorpion", "clockwork_scorpion", "tinplate_scorpion", "stinger_scorpion", "junkyard_scorpion"], "name_zh": "伏影沙蠍", "name_en": "The Duneshadow Scorpion", "class_archetype": "忍者 (Ninja)"}'

assert donkey_line in content, "donkey_line not found"
content = content.replace(
    donkey_line,
    donkey_line + ',\n\t\t\t\t' + scorpion_line,
    1
)

with open(gd_path, "w", encoding="utf-8") as f:
    f.write(content)

print("paperdoll_renderer.gd successfully updated for scorpion.")
