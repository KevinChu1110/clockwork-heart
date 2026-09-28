#!/usr/bin/env python3
from tools.build_kite_combat_poses import place_rotated_element, weapon_raw

b = place_rotated_element(weapon_raw, deg=-30, target_center=(80, 62), scale=0.96)
bbox = b.getbbox()
print("Hit bow bbox:", bbox, "margins:", bbox[0], bbox[1], 128 - bbox[2], 128 - bbox[3])
