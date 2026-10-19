#!/usr/bin/env python3
"""
tools/build_lion_maple_parts.py
Builds MapleStory-style Character.wz tight slice assets and origins for Lion (烈金雄獅).
Conforms to review.md 0-ART50 / 0-ART51 standards.
"""

import os
import numpy as np
from PIL import Image, ImageDraw

WS_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a"
SRC_DIR = f"{WS_ROOT}/game/assets/sprites/player/paperdoll/lion"
OUT_DIR = f"{SRC_DIR}/maple_parts"

def ensure_dirs():
    for sub in ["body", "head_unit", "eyes", "costume", "weapon", "winding_key", "back_curio"]:
        os.makedirs(f"{OUT_DIR}/{sub}", exist_ok=True)

def build_body_slices():
    print("--- 1. Building Body Slices ---")
    core_img = Image.open(f"{SRC_DIR}/optic_core/core_cyan_emerald_512.png").convert("RGBA")
    c_arr = np.array(core_img)
    # Extract only chest core (y >= 250), zeroing out eye area
    chest_only_arr = c_arr.copy()
    chest_only_arr[:250, :, :] = 0
    chest_core_img = Image.fromarray(chest_only_arr, mode="RGBA")

    for paint in ["paint_brass_gold", "paint_ivory_stock", "paint_midnight_navy"]:
        src_path = f"{SRC_DIR}/chassis/{paint}_512.png"
        chassis = Image.open(src_path).convert("RGBA")
        # Composite chassis with chest core
        body = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        body.alpha_composite(chassis)
        body.alpha_composite(chest_core_img)

        out_path = f"{OUT_DIR}/body/{paint}.png"
        body.save(out_path)
        print(f"  ✓ {out_path}: {body.size}, bbox={body.getbbox()}")

def build_head_unit_slices():
    print("--- 2. Building Head Unit Slices ---")
    # Mane bbox: (131, 51, 381, 281), size: (250, 230)
    # Neck anchor in 512: (250, 274) -> Origin: (250 - 131, 274 - 51) = (119, 223)
    crop_box = (131, 51, 381, 281)
    manes = [
        "ear_lion_gilded_mane_brass",
        "ear_lion_gilded_mane_ivory",
        "ear_lion_gilded_mane_midnight",
        "ear_lion_gilded_mane"
    ]
    for m in manes:
        src = f"{SRC_DIR}/head_unit/{m}_512.png"
        if not os.path.exists(src):
            src = f"{SRC_DIR}/head_unit/ear_lion_gilded_mane_512.png"
        im = Image.open(src).convert("RGBA")
        cropped = im.crop(crop_box)
        out_path = f"{OUT_DIR}/head_unit/{m}.png"
        cropped.save(out_path)
        print(f"  ✓ {out_path}: {cropped.size}, origin=[119, 223], bbox={cropped.getbbox()}")

def build_eyes_slices():
    print("--- 3. Building Eyes Slices ---")
    # Brow anchor in 512: (228, 173)
    # Crop canvas: 120 x 60 centered around (228, 173) -> (168, 143, 288, 203)
    # Origin: (60, 30)
    crop_box = (168, 143, 288, 203)

    eye_variants = [
        ("eyes_cyan_emerald", "core_cyan_emerald_512.png"),
        ("eyes_amber_gold", "core_amber_sun_512.png")
    ]

    for out_name, src_file in eye_variants:
        core_im = Image.open(f"{SRC_DIR}/optic_core/{src_file}").convert("RGBA")
        arr = np.array(core_im)
        # Strictly keep only eyes (y <= 195), remove any chest or stray noise pixels
        arr[195:, :, :] = 0
        cleaned_core = Image.fromarray(arr, mode="RGBA")
        cropped = cleaned_core.crop(crop_box)
        out_path = f"{OUT_DIR}/eyes/{out_name}.png"
        cropped.save(out_path)
        print(f"  ✓ {out_path}: {cropped.size}, origin=[60, 30], bbox={cropped.getbbox()}")

    # Build eyes_blink: closed eyelid curves matching centers at (25, 30) and (91, 30)
    blink_im = Image.new("RGBA", (120, 60), (0, 0, 0, 0))
    draw = ImageDraw.Draw(blink_im)
    outline_col = (40, 30, 60, 255)
    gold_highlight = (255, 208, 40, 220)

    # Left eye closed lid: center ~25, y ~30, span x: 16..34
    draw.arc([16, 25, 34, 35], start=0, end=180, fill=outline_col, width=3)
    draw.line([(15, 30), (35, 30)], fill=outline_col, width=2)
    draw.line([(18, 29), (32, 29)], fill=gold_highlight, width=1)

    # Right eye closed lid: center ~91, y ~30, span x: 80..102
    draw.arc([80, 25, 102, 35], start=0, end=180, fill=outline_col, width=3)
    draw.line([(79, 30), (103, 30)], fill=outline_col, width=2)
    draw.line([(82, 29), (100, 29)], fill=gold_highlight, width=1)

    out_blink = f"{OUT_DIR}/eyes/eyes_blink.png"
    blink_im.save(out_blink)
    print(f"  ✓ {out_blink}: {blink_im.size}, origin=[60, 30], bbox={blink_im.getbbox()}")

def build_costume_slices():
    print("--- 4. Building Costume Slices ---")
    # Costume crop: (130, 230, 370, 442) -> size (240, 212)
    # Navel anchor in 512: (256, 348) -> Origin: (256 - 130, 348 - 230) = (126, 118)
    crop_box = (130, 230, 370, 442)
    costumes = [
        ("costume_nutcracker_guard", "costume_nutcracker_guard_512.png"),
        ("costume_royal_guard", "costume_nutcracker_guard_512.png"), # Alias for royal guard armor
        ("costume_steam_artisan", "costume_steam_artisan_512.png")
    ]
    for out_name, src_file in costumes:
        im = Image.open(f"{SRC_DIR}/costume/{src_file}").convert("RGBA")
        cropped = im.crop(crop_box)
        out_path = f"{OUT_DIR}/costume/{out_name}.png"
        cropped.save(out_path)
        print(f"  ✓ {out_path}: {cropped.size}, origin=[126, 118], bbox={cropped.getbbox()}")

def build_weapon_slices():
    print("--- 5. Building Weapon Slices ---")
    # Weapon bbox: (75, 27, 153, 384) -> size (78, 357)
    # Hand anchor in 512: (144, 320) -> Origin: (144 - 75, 320 - 27) = (69, 293)
    crop_box = (75, 27, 153, 384)
    im = Image.open(f"{SRC_DIR}/weapon/wpn_knight_lance_512.png").convert("RGBA")
    cropped = im.crop(crop_box)
    out_path = f"{OUT_DIR}/weapon/wpn_knight_lance.png"
    cropped.save(out_path)
    print(f"  ✓ {out_path}: {cropped.size}, origin=[69, 293], bbox={cropped.getbbox()}")

def build_winding_key_slices():
    print("--- 6. Building Winding Key Slices ---")
    # Key bbox: (322, 183, 441, 333) -> size (119, 150)
    # Back key anchor in 512: (342, 296) -> Origin: (342 - 322, 296 - 183) = (20, 113)
    crop_box = (322, 183, 441, 333)
    im = Image.open(f"{SRC_DIR}/winding_key/key_classic_brass_512.png").convert("RGBA")
    cropped = im.crop(crop_box)
    out_path = f"{OUT_DIR}/winding_key/key_classic_brass.png"
    cropped.save(out_path)
    print(f"  ✓ {out_path}: {cropped.size}, origin=[20, 113], bbox={cropped.getbbox()}")

def build_back_curio_slices():
    print("--- 7. Building Back Curio Slices ---")
    tail_128 = Image.open(f"{SRC_DIR}/back_curio/curio_lion_fan_tail.png").convert("RGBA")
    tail_512 = tail_128.resize((512, 512), Image.Resampling.LANCZOS)
    # Tail bbox in 512 is (351, 364, 450, 458) -> size (99, 94)
    crop_box = (351, 364, 450, 458)
    cropped = tail_512.crop(crop_box)
    # Tail anchor relative to navel or root: in 512 attachment is at (360, 380)
    # Origin: (360 - 351, 380 - 364) = (9, 16)
    out_path = f"{OUT_DIR}/back_curio/curio_lion_fan_tail.png"
    cropped.save(out_path)
    print(f"  ✓ {out_path}: {cropped.size}, origin=[9, 16], bbox={cropped.getbbox()}")

if __name__ == "__main__":
    ensure_dirs()
    build_body_slices()
    build_head_unit_slices()
    build_eyes_slices()
    build_costume_slices()
    build_weapon_slices()
    build_winding_key_slices()
    build_back_curio_slices()
    print("🎉 All Lion MapleStory-style slices built successfully!")
