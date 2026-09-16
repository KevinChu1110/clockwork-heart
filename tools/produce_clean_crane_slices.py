#!/usr/bin/env python3
"""
produce_clean_crane_slices.py
Definitive production & verification tool for the 7 Cloud Crane paperdoll slices.
Modeled after produce_clean_tiger_slices.py.
"""

import os
from PIL import Image, ImageDraw

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/crane"

def main():
    print("=== PRODUCING CLEAN CLOUD CRANE PAPERDOLL SLICES ===")
    
    canonical_slots = [
        ("winding_key", 5, "key_tri_wing_zephyr.png"),
        ("back_curio", 8, "curio_origami_crane.png"),
        ("chassis", 10, "paint_crane_porcelain.png"),
        ("head_unit", 20, "head_cloud_crane_stock.png"),
        ("costume", 25, "costume_zephyr_robe.png"),
        ("optic_core", 30, "core_vermilion_lens.png"),
        ("weapon", 40, "wpn_zephyr_wing_bow.png"),
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
        
    proof_comp_path = f"{BASE_DIR}/proof_paperdoll_crane_composite.png"
    comp.save(proof_comp_path)
    print(f"  ✓ Composite saved to {proof_comp_path}, bbox: {comp.getbbox()}")
    
    # 3. Composite on magenta
    mag = Image.new("RGBA", (128, 128), (255, 0, 255, 255))
    mag.alpha_composite(comp)
    proof_mag_path = f"{BASE_DIR}/proof_paperdoll_crane_magenta.png"
    mag.save(proof_mag_path)
    print(f"  ✓ Magenta test saved to {proof_mag_path}")

    # 4. Verification crops (scaled up for visual inspection)
    crops = [
        ("verification_crop_head.png", (36, 10, 88, 58)),
        ("verification_crop_eyes.png", (58, 32, 80, 46)),
        ("verification_crop_key.png", (28, 30, 48, 58)),
        ("verification_crop_curio.png", (10, 20, 42, 48)),
        ("verification_crop_costume.png", (40, 52, 88, 96)),
        ("verification_crop_core.png", (56, 58, 74, 76)),
        ("verification_crop_weapon.png", (76, 48, 110, 104)),
        ("verification_crop_feet.png", (38, 98, 92, 126)),
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

    board_path = f"{BASE_DIR}/proof_crane_all_7_slices.png"
    board.save(board_path)
    print(f"  ✓ All verification proofs and visual board saved to {BASE_DIR}")

if __name__ == "__main__":
    main()
