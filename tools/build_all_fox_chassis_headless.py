#!/usr/bin/env python3
"""
tools/build_all_fox_chassis_headless.py
Updates the three Fox chassis assets (paint_fox_orange, paint_ivory_stock, paint_emerald_glaze):
- Erases head, ears, face, and chin slices from 512 and 128 chassis assets.
- Leaves intact: neck and below body, limbs, tail, wind-up key, chest core.
- Produces clean metallic neck collar socket for modular head attachment.
- Uses LANCZOS for 128 downsampling and strictly avoids NEAREST fake upscaling.
"""

import os
import numpy as np
from PIL import Image

REPO_ROOT = os.environ.get("HERMES_KANBAN_WORKSPACE", os.getcwd())
CHASSIS_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/chassis"

VARIANTS = {
    "paint_fox_orange": {
        "rim_dark": (22, 16, 10, 255),
        "metal_mid": (111, 57, 8, 255),
        "metal_bright": (145, 80, 20, 255),
        "socket_dark": (35, 20, 8, 255),
    },
    "paint_ivory_stock": {
        "rim_dark": (25, 24, 22, 255),
        "metal_mid": (120, 116, 107, 255),
        "metal_bright": (155, 150, 140, 255),
        "socket_dark": (40, 38, 35, 255),
    },
    "paint_emerald_glaze": {
        "rim_dark": (10, 25, 18, 255),
        "metal_mid": (17, 111, 65, 255),
        "metal_bright": (35, 145, 90, 255),
        "socket_dark": (12, 40, 22, 255),
    },
}

def process_variant(var_name: str, config: dict):
    src_512_p = f"{CHASSIS_DIR}/{var_name}_512.png"
    src = Image.open(src_512_p).convert("RGBA")
    arr = np.array(src)
    h, w, _ = arr.shape
    
    rim_dark = config["rim_dark"]
    metal_mid = config["metal_mid"]
    metal_bright = config["metal_bright"]
    socket_dark = config["socket_dark"]
    
    # Calculate boundary array for each x
    y_bound = np.zeros(w, dtype=int)
    for x in range(w):
        if x < 170:
            y_bound[x] = 320
        elif x < 224:
            # Left flank: smooth transition down to y=268 at x=224
            t = (x - 170.0) / 54.0
            y_bound[x] = int(round(285.0 - 17.0 * t))
        elif x <= 307:
            # Collar zone: center at 265.5, rx=41.5
            norm_x = (x - 265.5) / 41.5
            top_cy = 268.0 - 16.0 * np.sqrt(max(0.0, 1.0 - norm_x**2))
            y_bound[x] = int(round(top_cy))
        elif x <= 360:
            t = (x - 307.0) / 53.0
            y_bound[x] = int(round(268.0 - 13.0 * t))
        elif x <= 375:
            t = (x - 360.0) / 15.0
            y_bound[x] = int(round(255.0 - 13.0 * t))
        elif x <= 388:
            y_bound[x] = 242
        elif x <= 435:
            y_bound[x] = 237
        else:
            y_bound[x] = 330
            
    out = np.copy(arr)
    # Erase everything above y_bound
    for x in range(w):
        yb = y_bound[x]
        out[:yb, x, :] = 0
        
    # In the collar zone (x in [224..307]), fill collar socket down to y=267
    for x in range(224, 308):
        norm_x = (x - 265.5) / 41.5
        if abs(norm_x) <= 1.0:
            top_cy = 268.0 - 16.0 * np.sqrt(1.0 - norm_x**2)
            y_start = int(round(top_cy))
            for y in range(y_start, 268):
                dist = y - top_cy
                if dist <= 1.8:
                    out[y, x] = rim_dark
                elif dist <= 4.0:
                    out[y, x] = metal_bright
                elif dist <= 7.0:
                    out[y, x] = metal_mid
                else:
                    out[y, x] = socket_dark
                    
    # Smooth continuous dark outer rim line along the collar curve
    for x in range(223, 309):
        norm_x = (x - 265.5) / 41.5
        if abs(norm_x) <= 1.0:
            top_cy = int(round(268.0 - 16.0 * np.sqrt(1.0 - norm_x**2)))
            if 0 <= top_cy < h:
                out[top_cy, x] = rim_dark

    # Save 512
    img_512 = Image.fromarray(out)
    img_512.save(src_512_p, format="PNG")
    print(f"✓ Saved {src_512_p} (512x512)")
    
    # Generate 128 downsampled version via strict LANCZOS
    dst_128_p = f"{CHASSIS_DIR}/{var_name}.png"
    img_128 = img_512.resize((128, 128), resample=Image.Resampling.LANCZOS)
    img_128.save(dst_128_p, format="PNG")
    print(f"✓ Saved {dst_128_p} (128x128 via LANCZOS)")

def main():
    for name, cfg in VARIANTS.items():
        process_variant(name, cfg)

if __name__ == "__main__":
    main()
