#!/usr/bin/env python3
"""
tools/generate_bear_penguin_head_variants.py
Definitive production generator for Head Unit paint variants:
- Bear: Amber, Quarry, Ivory (stock)
- Penguin: Navy (stock), Ivory, Polar Frost

100% preserves authentic hand-painted outlines, goggles, beaks, rivets, and lenses.
Uses continuous smooth cel-shading gradients with zero stepping artifacts or artificial patches.
"""

import os
import numpy as np
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"

BEAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bear"
PENGUIN_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/penguin"

# --- Palettes ---

BEAR_RAMPS = {
    "amber": {
        "P_DEEP":   (108, 48, 15),
        "P_SHADOW": (165, 80, 20),      # Exact chassis dominant color
        "P_MID":    (195, 105, 28),
        "P_LIGHT":  (224, 126, 38),
        "P_SPEC":   (250, 175, 85),
        # Muzzle secondary: warm honey/caramel cream
        "S_DEEP":   (130, 70, 22),
        "S_SHADOW": (175, 100, 35),
        "S_MID":    (215, 140, 60),
        "S_LIGHT":  (240, 185, 115),
        "S_SPEC":   (255, 220, 160),
    },
    "quarry": {
        "P_DEEP":   (28, 36, 52),
        "P_SHADOW": (48, 62, 86),       # Exact chassis dominant color
        "P_MID":    (72, 92, 122),
        "P_LIGHT":  (105, 132, 168),
        "P_SPEC":   (155, 182, 218),
        # Muzzle secondary: cool slate white
        "S_DEEP":   (55, 68, 90),
        "S_SHADOW": (95, 115, 145),
        "S_MID":    (150, 172, 200),
        "S_LIGHT":  (205, 222, 242),
        "S_SPEC":   (240, 248, 255),
    },
    "ivory": {
        "P_DEEP":   (138, 124, 104),
        "P_SHADOW": (185, 170, 148),    # Exact chassis dominant color
        "P_MID":    (212, 198, 175),
        "P_LIGHT":  (235, 224, 205),
        "P_SPEC":   (252, 246, 235),
        # Muzzle secondary: soft ivory enamel
        "S_DEEP":   (150, 135, 115),
        "S_SHADOW": (195, 180, 158),
        "S_MID":    (225, 215, 195),
        "S_LIGHT":  (245, 238, 225),
        "S_SPEC":   (255, 252, 245),
    }
}

PENGUIN_RAMPS = {
    "navy": {
        "c4": (14, 25, 65),
        "c3": (20, 38, 95),
        "c2": (30, 58, 138),     # Exact chassis dominant color
        "c1": (48, 95, 192),
        "c0": (75, 140, 245),
    },
    "polar": {
        "c4": (185, 210, 230),
        "c3": (210, 228, 245),
        "c2": (235, 245, 252),
        "c1": (248, 252, 255),
        "c0": (255, 255, 255),   # Exact chassis dominant highlight
    },
    "ivory": {
        "c4": (145, 132, 115),
        "c3": (198, 185, 165),
        "c2": (235, 226, 210),   # Exact chassis dominant color
        "c1": (252, 248, 238),
        "c0": (255, 255, 255),
    }
}

def interpolate_stops(val, stops: list[tuple[int, int, int]]) -> tuple[int, int, int]:
    t = float(np.clip(float(val), 0.0, 1.0))
    n = len(stops) - 1
    idx = int(t * n)
    if idx >= n:
        return stops[-1]
    u = (t * n) - idx
    c1 = stops[idx]
    c2 = stops[idx + 1]
    return (
        int(round(c1[0] + u * (c2[0] - c1[0]))),
        int(round(c1[1] + u * (c2[1] - c1[1]))),
        int(round(c1[2] + u * (c2[2] - c1[2])))
    )

def build_penguin_head_variants():
    src_p = f"{PENGUIN_DIR}/head_unit/head_steam_penguin_stock_512.png"
    im = Image.open(src_p).convert("RGBA")
    arr = np.array(im)
    alpha = arr[:, :, 3]
    rgb = arr[:, :, :3].astype(float)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]

    is_outline = (alpha > 50) & (r < 40) & (g < 40) & (b < 50)
    is_goggles_frame = (alpha > 50) & (r > 150) & (g > 100) & (b < 120)
    is_goggles_lens = (alpha > 50) & (g > 140) & (b > 160) & (r < 120)
    is_beak = (alpha > 50) & (r > 180) & (g > 100) & (b < 60)
    is_strap = (alpha > 50) & (r > 70) & (r < 165) & (g > 40) & (g < 105) & (b < 75)

    y_indices, x_indices = np.indices(arr.shape[:2])
    is_cap = (alpha > 50) & (~is_outline) & (~is_goggles_frame) & (~is_goggles_lens) & (~is_beak) & (~is_strap)
    is_blue_cap = is_cap & ((b >= r) | (y_indices < 110))

    lum = 0.299 * r + 0.587 * g + 0.114 * b
    cap_t = np.clip((lum - 20.0) / (150.0 - 20.0), 0.0, 1.0)

    for variant in ["ivory", "polar"]:
        stops = [
            PENGUIN_RAMPS[variant]["c4"],
            PENGUIN_RAMPS[variant]["c3"],
            PENGUIN_RAMPS[variant]["c2"],
            PENGUIN_RAMPS[variant]["c1"],
            PENGUIN_RAMPS[variant]["c0"],
        ]
        var_arr = arr.copy()

        for y, x in zip(*np.where(is_blue_cap)):
            t = cap_t[y, x]
            col = interpolate_stops(t, stops)
            var_arr[y, x, 0] = col[0]
            var_arr[y, x, 1] = col[1]
            var_arr[y, x, 2] = col[2]

        out_512 = f"{PENGUIN_DIR}/head_unit/head_steam_penguin_{variant}_512.png"
        out_im_512 = Image.fromarray(var_arr, "RGBA")
        out_im_512.save(out_512, "PNG")
        print(f"✓ Saved Penguin 512: {out_512}")

        out_128 = f"{PENGUIN_DIR}/head_unit/head_steam_penguin_{variant}.png"
        out_im_128 = out_im_512.resize((128, 128), resample=Image.Resampling.LANCZOS)
        out_im_128.save(out_128, "PNG")
        print(f"✓ Saved Penguin 128: {out_128}")

    navy_alias_512 = f"{PENGUIN_DIR}/head_unit/head_steam_penguin_navy_512.png"
    im.save(navy_alias_512, "PNG")
    navy_alias_128 = f"{PENGUIN_DIR}/head_unit/head_steam_penguin_navy.png"
    im.resize((128, 128), resample=Image.Resampling.LANCZOS).save(navy_alias_128, "PNG")
    print(f"✓ Saved Penguin Navy alias 512/128")

def build_bear_head_variants():
    src_p = f"{BEAR_DIR}/head_unit/head_iron_bear_stock_512.png"
    im = Image.open(src_p).convert("RGBA")
    arr = np.array(im)
    alpha = arr[:, :, 3]
    rgb = arr[:, :, :3].astype(float)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]

    # Preserve features:
    is_outline = (alpha > 50) & (r < 40) & (g < 40) & (b < 50)
    is_green_eye = (alpha > 50) & (g > 140) & (g > r + 30) & (g > b + 20)
    is_brass = (alpha > 50) & (r > 180) & (g > 130) & (b < 100) & (r > b + 80)
    is_dark_socket = (alpha > 50) & (r < 60) & (g < 60) & (b < 75)

    y_idx, x_idx = np.indices(arr.shape[:2])
    # Snout cover / muzzle plate (centered around x: 230..280, y: 155..205)
    is_muzzle_box = (x_idx >= 230) & (x_idx <= 280) & (y_idx >= 155) & (y_idx <= 205)
    is_muzzle = is_muzzle_box & (alpha > 50) & (~is_outline) & (~is_brass) & (~is_dark_socket)
    
    # Primary plates: ALL remaining head plates (forehead, crown, cheeks, ears, jaw)
    is_primary = (alpha > 50) & (~is_outline) & (~is_green_eye) & (~is_brass) & (~is_dark_socket) & (~is_muzzle)

    lum = 0.299 * r + 0.587 * g + 0.114 * b
    prim_t = np.clip((lum - 50.0) / (240.0 - 50.0), 0.0, 1.0)
    muzzle_t = np.clip((lum - 60.0) / (240.0 - 60.0), 0.0, 1.0)

    for variant in ["amber", "quarry", "ivory"]:
        var_arr = arr.copy()
        ramp = BEAR_RAMPS[variant]

        p_stops = [
            ramp["P_DEEP"],
            ramp["P_SHADOW"],
            ramp["P_SHADOW"],
            ramp["P_MID"],
            ramp["P_LIGHT"],
        ]
        s_stops = [
            ramp["S_DEEP"],
            ramp["S_SHADOW"],
            ramp["S_MID"],
            ramp["S_LIGHT"],
            ramp["S_SPEC"]
        ]

        # Recolor primary plates (forehead, cheeks, ears, jaw)
        for y, x in zip(*np.where(is_primary)):
            col = interpolate_stops(prim_t[y, x], p_stops)
            var_arr[y, x, 0] = col[0]
            var_arr[y, x, 1] = col[1]
            var_arr[y, x, 2] = col[2]

        # Recolor muzzle plate in harmonious secondary tone
        for y, x in zip(*np.where(is_muzzle)):
            col = interpolate_stops(muzzle_t[y, x], s_stops)
            var_arr[y, x, 0] = col[0]
            var_arr[y, x, 1] = col[1]
            var_arr[y, x, 2] = col[2]

        if variant == "ivory":
            out_512 = f"{BEAR_DIR}/head_unit/head_iron_bear_stock_512.png"
            alias_512 = f"{BEAR_DIR}/head_unit/head_iron_bear_ivory_512.png"
            out_128 = f"{BEAR_DIR}/head_unit/head_iron_bear_stock.png"
            alias_128 = f"{BEAR_DIR}/head_unit/head_iron_bear_ivory.png"
        else:
            out_512 = f"{BEAR_DIR}/head_unit/head_iron_bear_{variant}_512.png"
            alias_512 = None
            out_128 = f"{BEAR_DIR}/head_unit/head_iron_bear_{variant}.png"
            alias_128 = None

        out_im_512 = Image.fromarray(var_arr, "RGBA")
        out_im_512.save(out_512, "PNG")
        print(f"✓ Saved Bear 512: {out_512}")
        if alias_512:
            out_im_512.save(alias_512, "PNG")

        out_im_128 = out_im_512.resize((128, 128), resample=Image.Resampling.LANCZOS)
        out_im_128.save(out_128, "PNG")
        print(f"✓ Saved Bear 128: {out_128}")
        if alias_128:
            out_im_128.save(alias_128, "PNG")

if __name__ == "__main__":
    print("=== Generating Penguin Head Variants ===")
    build_penguin_head_variants()
    print("\n=== Generating Bear Head Variants ===")
    build_bear_head_variants()
