#!/usr/bin/env python3
"""
produce_clean_bear_slices.py
Definitive production & verification tool for the 7 The Iron Bear paperdoll slices.
Modeled after produce_clean_crane_slices.py and produce_clean_tiger_slices.py.
"""

import os
from PIL import Image, ImageDraw

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bear"

def main():
    print("=== PRODUCING CLEAN IRON BEAR PAPERDOLL SLICES ===")
    
    canonical_slots = [
        ("winding_key", 5, "key_cross_pendulum.png"),
        ("back_curio", 8, "curio_music_honey_cask.png"),
        ("chassis", 10, "paint_bear_amber.png"),
        ("head_unit", 20, "head_iron_bear_stock.png"),
        ("costume", 25, "costume_ironclad_overalls.png"),
        ("optic_core", 30, "core_emerald_lens.png"),
        ("weapon", 40, "wpn_eccentric_gyro_sledge.png"),
    ]
    
    # 1. Verify all 7 canonical slices exist and are 128x128 RGBA
    for slot_id, z, fname in canonical_slots:
        p = f"{BASE_DIR}/{slot_id}/{fname}"
        assert os.path.exists(p), f"Missing slice: {p}"
        im = Image.open(p)
        assert im.size == (128, 128), f"Wrong size {im.size} for {p}"
        assert im.mode == "RGBA", f"Wrong mode {im.mode} for {p}"
        bbox = im.getbbox()
        assert bbox is not None, f"Slice is completely transparent: {p}"
        print(f"  ✓ {slot_id:12s} (Z:{z:2d}) -> {fname} (bbox: {bbox})")

    # 2. Build composite
    comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    for slot_id, z, fname in canonical_slots:
        layer = Image.open(f"{BASE_DIR}/{slot_id}/{fname}").convert("RGBA")
        comp.alpha_composite(layer)
        
    proof_comp_path = f"{BASE_DIR}/proof_paperdoll_bear_composite.png"
    comp.save(proof_comp_path)
    print(f"  ✓ Composite saved to {proof_comp_path}, bbox: {comp.getbbox()}")
    
    # 3. Composite on magenta
    mag = Image.new("RGBA", (128, 128), (255, 0, 255, 255))
    mag.alpha_composite(comp)
    proof_mag_path = f"{BASE_DIR}/proof_paperdoll_bear_magenta.png"
    mag.save(proof_mag_path)
    print(f"  ✓ Magenta test saved to {proof_mag_path}")

    # 4. Verification crops (scaled up for visual inspection)
    crops = [
        ("verification_crop_head.png", (24, 16, 104, 62)),
        ("verification_crop_ears.png", (25, 18, 102, 38)),
        ("verification_crop_eyes.png", (48, 33, 80, 45)),
        ("verification_crop_nose.png", (52, 42, 76, 56)),
        ("verification_crop_key.png", (8, 20, 46, 60)),
        ("verification_crop_curio.png", (94, 12, 116, 40)),
        ("verification_crop_costume.png", (40, 56, 88, 96)),
        ("verification_crop_core.png", (56, 62, 72, 78)),
        ("verification_crop_weapon.png", (74, 44, 116, 115)),
        ("verification_crop_feet.png", (36, 110, 90, 126)),
    ]

    for cname, box in crops:
        c_img = comp.crop(box)
        scale_factor = max(1, 400 // max(c_img.size))
        c_large = c_img.resize((c_img.width * scale_factor, c_img.height * scale_factor), Image.Resampling.NEAREST)
        c_large.save(f"{BASE_DIR}/{cname}")

    # 5. Visual board: all 7 slices side by side
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

    board_path = f"{BASE_DIR}/proof_bear_all_7_slices.png"
    board.save(board_path)
    print(f"  ✓ All verification proofs and visual board saved to {BASE_DIR}")

if __name__ == "__main__":
    main()
