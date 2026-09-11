#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from typing import cast
from PIL import Image

def check_hands():
    body_clean = Image.open("/tmp/fox_test/char_no_shadow_no_wep.png").convert("RGBA")
    staff_src = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
    
    b_px = body_clean.load()
    s_px = staff_src.load()
    assert b_px is not None and s_px is not None
    
    print("body_clean around (85..95, 80..95):")
    for y in range(80, 95):
        row = [f"{x}" for x in range(85, 98) if cast(tuple[int,int,int,int], b_px[x, y])[3] > 40]
        if row:
            print(f"y={y}: " + " ".join(row))

    print("\nstaff_src around (85..95, 80..95):")
    for y in range(80, 95):
        row = [f"{x}" for x in range(85, 98) if cast(tuple[int,int,int,int], s_px[x, y])[3] > 40]
        if row:
            print(f"y={y}: " + " ".join(row))

if __name__ == "__main__":
    check_hands()
