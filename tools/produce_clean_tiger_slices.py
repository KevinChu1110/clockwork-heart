#!/usr/bin/env python3
"""
produce_clean_tiger_slices.py
Definitive production tool for the 7 Ember Tiger paperdoll slices.
"""

import os
from PIL import Image, ImageDraw, ImageChops
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/tiger"
KEY_UNIV_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_UNIV_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

def main():
    print("=== PRODUCING CLEAN EMBER TIGER PAPERDOLL SLICES ===")
    
    canonical_slots = [
        ("winding_key", 5, "key_turbine_flame.png"),
        ("back_curio", 8, "curio_exhaust_tiger_tail.png"),
        ("chassis", 10, "paint_ember_orange.png"),
        ("head_unit", 20, "head_ember_tiger_stock.png"),
        ("costume", 25, "costume_ember_tunic.png"),
        ("optic_core", 30, "core_molten_amber.png"),
        ("weapon", 40, "wpn_twin_ember_sabers.png"),
    ]
    
    # Verify all 7 canonical slices exist and are 128x128 RGBA
    for slot_id, z, fname in canonical_slots:
        p = f"{BASE_DIR}/{slot_id}/{fname}"
        assert os.path.exists(p), f"Missing slice: {p}"
        im = Image.open(p)
        assert im.size == (128, 128), f"Wrong size {im.size} for {p}"
        assert im.mode == "RGBA", f"Wrong mode {im.mode} for {p}"
        bbox = im.getbbox()
        assert bbox is not None, f"Slice is completely transparent: {p}"
        print(f"  ✓ {slot_id:12s} (Z:{z:2d}) -> {fname} (bbox: {bbox})")

    # Verify composite
    comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    for slot_id, z, fname in canonical_slots:
        layer = Image.open(f"{BASE_DIR}/{slot_id}/{fname}").convert("RGBA")
        comp.alpha_composite(layer)
        
    proof_comp_path = f"{BASE_DIR}/proof_paperdoll_tiger_composite.png"
    comp.save(proof_comp_path)
    
    mag = Image.new("RGBA", (128, 128), (255, 0, 255, 255))
    mag.alpha_composite(comp)
    proof_mag_path = f"{BASE_DIR}/proof_paperdoll_tiger_magenta.png"
    mag.save(proof_mag_path)

    # Verification crops
    crops = [
        ("verification_crop_ears.png", (28, 6, 98, 36)),
        ("verification_crop_forehead.png", (50, 18, 76, 38)),
        ("verification_crop_eyes.png", (46, 28, 82, 48)),
        ("verification_crop_key.png", (16, 36, 48, 68)),
        ("verification_crop_tail.png", (10, 48, 42, 108)),
        ("verification_crop_weapon.png", (72, 44, 122, 106)),
        ("verification_crop_costume.png", (42, 50, 84, 96)),
    ]

    for cname, box in crops:
        c_img = comp.crop(box)
        scale_factor = max(1, 400 // max(c_img.size))
        c_large = c_img.resize((c_img.width * scale_factor, c_img.height * scale_factor), Image.Resampling.NEAREST)
        c_large.save(f"{BASE_DIR}/{cname}")

    # Visual board
    board = Image.new("RGBA", (7 * 140 + 20, 180), (28, 24, 40, 255))
    b_draw = ImageDraw.Draw(board)
    for i, (slot_id, z, fname) in enumerate(canonical_slots):
        p = f"{BASE_DIR}/{slot_id}/{fname}"
        img = Image.open(p).convert("RGBA")
        x = 10 + i * 140
        y = 10
        b_draw.rounded_rectangle((x, y, x + 128, y + 128), radius=6, fill=(45, 38, 58, 255), outline=(90, 75, 110, 255))
        board.alpha_composite(img, (x, y))
        tb = b_draw.textbbox((0, 0), slot_id)
        tw = tb[2] - tb[0]
        b_draw.text((x + (128 - tw) // 2, y + 135), slot_id, fill=(255, 215, 64, 255))

    board_path = f"{BASE_DIR}/proof_tiger_all_7_slices.png"
    board.save(board_path)
    print(f"✓ All verification proofs and visual board saved to {BASE_DIR}")

if __name__ == "__main__":
    main()
