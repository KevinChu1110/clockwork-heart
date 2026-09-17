#!/usr/bin/env python3
"""
tools/build_all_macaque_chassis_headless.py
Updates the two Macaque chassis assets (paint_bamboo_bronze, paint_ivory_stock):
- Erases head, ears, face, and chin slices from 512 and 128 chassis assets.
- Leaves intact: neck and below body, limbs, tail, wind-up key, chest core.
- Produces clean metallic neck collar socket for modular head attachment.
- Eliminates stray pixels and secondary ears for clean edges.
- Uses LANCZOS for 128 downsampling and strictly avoids NEAREST fake upscaling.
"""

import os
import numpy as np
from PIL import Image

REPO_ROOT = os.environ.get("HERMES_KANBAN_WORKSPACE", os.getcwd())
CHASSIS_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque/chassis"

VARIANTS = {
    "paint_bamboo_bronze": {
        "rim_dark": (24, 18, 54, 255),
        "metal_bright": (240, 195, 85, 255),
        "metal_mid": (195, 150, 50, 255),
        "socket_dark": (45, 35, 30, 255),
    },
    "paint_ivory_stock": {
        "rim_dark": (28, 21, 38, 255),
        "metal_bright": (235, 225, 205, 255),
        "metal_mid": (175, 150, 130, 255),
        "socket_dark": (50, 42, 45, 255),
    },
}

def clean_and_build_all():
    for var_name, config in VARIANTS.items():
        src_path = f"{CHASSIS_DIR}/{var_name}_512.png"
        src = Image.open(src_path).convert("RGBA")
        arr = np.array(src)
        h, w, _ = arr.shape
        
        rim_dark = config["rim_dark"]
        metal_bright = config["metal_bright"]
        metal_mid = config["metal_mid"]
        socket_dark = config["socket_dark"]
        
        # Calculate boundary array for each x
        y_bound = np.zeros(w, dtype=int)
        for x in range(w):
            if x < 118:
                # Left flank empty space
                y_bound[x] = 330
            elif x < 145:
                # Left forearm
                t = (x - 118.0) / 27.0
                y_bound[x] = int(round(320.0 - 21.0 * t))
            elif x < 168:
                # Left upper arm / shoulder
                t = (x - 145.0) / 23.0
                y_bound[x] = int(round(299.0 - 31.0 * t))
            elif x < 184:
                # Left shoulder to collar connection
                t = (x - 168.0) / 16.0
                y_bound[x] = int(round(268.0 - 8.0 * t))
            elif x <= 288:
                # Collar zone: center at 236.0, rx=52.0
                norm_x = (x - 236.0) / 52.0
                top_cy = 264.0 - 10.0 * np.sqrt(max(0.0, 1.0 - norm_x**2))
                y_bound[x] = int(round(top_cy))
            elif x <= 304:
                # Transition from collar right edge to winding key base
                t = (x - 288.0) / 16.0
                y_bound[x] = int(round(264.0 - 38.0 * t))
            elif x <= 334:
                # Winding key loop: top at y=226
                norm_k = (x - 320.0) / 14.0
                top_ky = 230.0 - 4.0 * np.sqrt(max(0.0, 1.0 - min(1.0, norm_k**2)))
                y_bound[x] = int(round(top_ky))
            elif x <= 356:
                # Dip between key and right arm
                t = (x - 334.0) / 22.0
                y_bound[x] = int(round(230.0 - 2.0 * t))
            elif x <= 374:
                # Right arm top
                y_bound[x] = 228
            else:
                # Right ear boundary: clear all secondary right ear pixels above y=265
                y_bound[x] = 265
                
        out = np.copy(arr)
        # Erase everything above y_bound
        for x in range(w):
            yb = y_bound[x]
            out[:yb, x, :] = 0
            
        # Clean any stray pixels above 225
        out[:225, :, :] = 0
        
        # Clean secondary right ear stray pixels (x >= 375, y < 265)
        out[:265, 375:, :] = 0
        
        # Clean left ear stray pixels (x < 165, y < 275)
        out[:275, :165, :] = 0
        
        # Clean nearly invisible stray pixels with alpha < 10
        out[out[:, :, 3] < 10] = 0
        
        # Render clean metallic collar socket in the collar zone (x in [184..288])
        for x in range(184, 289):
            norm_x = (x - 236.0) / 52.0
            if abs(norm_x) <= 1.0:
                top_cy = 264.0 - 10.0 * np.sqrt(1.0 - norm_x**2)
                y_start = int(round(top_cy))
                for y in range(y_start, 266):
                    dist = y - top_cy
                    if dist <= 1.8:
                        out[y, x] = rim_dark
                    elif dist <= 3.8:
                        out[y, x] = metal_bright
                    elif dist <= 5.8:
                        out[y, x] = metal_mid
                    else:
                        out[y, x] = socket_dark
                        
        # Smooth continuous outer rim line along collar curve
        for x in range(183, 290):
            norm_x = (x - 236.0) / 52.0
            if abs(norm_x) <= 1.0:
                top_cy = int(round(264.0 - 10.0 * np.sqrt(1.0 - norm_x**2)))
                if 0 <= top_cy < h:
                    out[top_cy, x] = rim_dark

        # Save 512
        src_512_p = f"{CHASSIS_DIR}/{var_name}_512.png"
        img_512 = Image.fromarray(out)
        img_512.save(src_512_p, format="PNG")
        print(f"✓ Saved {src_512_p} (512x512)")
        
        # Generate 128 downsampled version via strict LANCZOS
        dst_128_p = f"{CHASSIS_DIR}/{var_name}.png"
        img_128 = img_512.resize((128, 128), resample=Image.Resampling.LANCZOS)
        img_128.save(dst_128_p, format="PNG")
        print(f"✓ Saved {dst_128_p} (128x128 via LANCZOS)")

if __name__ == "__main__":
    clean_and_build_all()
