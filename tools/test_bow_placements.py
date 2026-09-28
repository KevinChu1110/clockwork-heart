#!/usr/bin/env python3
from tools.build_kite_combat_poses import place_rotated_element, weapon_raw

tests = [
    ("idle", 0, (102, 69), 0.98),
    ("tele", -24, (92, 66), 0.98),
    ("atk", -12, (96, 66), 0.98),
    ("recover", -10, (93, 65), 0.96),
    ("skill", -52, (88, 62), 0.96),
    ("hit", -36, (84, 63), 0.97),
]

for name, deg, center, sc in tests:
    b = place_rotated_element(weapon_raw, deg=deg, target_center=center, scale=sc)
    bbox = b.getbbox()
    assert bbox is not None
    left = bbox[0]
    top = bbox[1]
    right = 128 - bbox[2]
    bot = 128 - bbox[3]
    print(f"{name:10s}: deg={deg:3d}, center={center}, bbox={bbox}, margins: L={left}, T={top}, R={right}, B={bot}, y2={bbox[3]}")
