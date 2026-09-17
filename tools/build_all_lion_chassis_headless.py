#!/usr/bin/env python3
"""
tools/build_all_lion_chassis_headless.py
Updates the three Lion chassis assets (paint_brass_gold, paint_ivory_stock, paint_midnight_navy):
- Erases head, ears, face, and chin slices from 512 and 128 chassis assets.
- Leaves intact: neck and below body, limbs, tail, wind-up key, chest core.
- Produces clean metallic neck collar socket for modular head attachment.
- Eliminates stray pixels and floating fragments for clean edges.
- Uses LANCZOS for 128 downsampling and strictly avoids NEAREST fake upscaling.
"""

import os
import subprocess
import io
import numpy as np
from PIL import Image

REPO_ROOT = os.environ.get("HERMES_KANBAN_WORKSPACE", os.getcwd())
CHASSIS_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/lion/chassis"

VARIANTS = {
    "paint_brass_gold": {
        "rim_dark": (39, 27, 26, 255),
        "metal_mid": (190, 160, 120, 255),
        "metal_bright": (238, 220, 175, 255),
        "socket_dark": (65, 45, 30, 255),
    },
    "paint_ivory_stock": {
        "rim_dark": (28, 21, 38, 255),
        "metal_mid": (180, 175, 170, 255),
        "metal_bright": (245, 242, 235, 255),
        "socket_dark": (50, 48, 55, 255),
    },
    "paint_midnight_navy": {
        "rim_dark": (23, 23, 44, 255),
        "metal_mid": (70, 100, 145, 255),
        "metal_bright": (165, 200, 225, 255),
        "socket_dark": (35, 45, 70, 255),
    },
}

def clean_and_build_all():
    for var_name, config in VARIANTS.items():
        # Get raw image from git HEAD
        cmd = ["git", "show", f"HEAD:game/assets/sprites/player/paperdoll/lion/chassis/{var_name}_512.png"]
        p = subprocess.run(cmd, capture_output=True, check=True)
        src = Image.open(io.BytesIO(p.stdout)).convert("RGBA")
        arr = np.array(src)
        h, w, _ = arr.shape
        
        rim_dark = config["rim_dark"]
        metal_mid = config["metal_mid"]
        metal_bright = config["metal_bright"]
        socket_dark = config["socket_dark"]
        
        # Calculate boundary array for each x
        y_bound = np.zeros(w, dtype=int)
        for x in range(w):
            if x < 187:
                # Clear all stray fragments on left flank above y=290
                y_bound[x] = 290
            elif x < 195:
                # Transition from left flank (y=284 at 187) to collar edge (y=276 at 195)
                t = (x - 187.0) / (195.0 - 187.0)
                y_bound[x] = int(round(284.0 - 8.0 * t))
            elif x <= 285:
                # Collar zone: center at 240.0, rx=45.0
                norm_x = (x - 240.0) / 45.0
                top_cy = 276.0 - 12.0 * np.sqrt(max(0.0, 1.0 - norm_x**2))
                y_bound[x] = int(round(top_cy))
            elif x <= 330:
                # Transition from collar right edge to right shoulder
                t = (x - 285.0) / (330.0 - 285.0)
                y_bound[x] = int(round(276.0 + 4.0 * t))
            elif x <= 389:
                # Right shoulder / arm area
                y_bound[x] = 280
            else:
                # Remove stray 3px line at x >= 390
                y_bound[x] = 330
                
        out = np.copy(arr)
        # Erase everything above y_bound
        for x in range(w):
            yb = y_bound[x]
            out[:yb, x, :] = 0
            
        # Clean isolated stray pixels in x >= 390 up to y=330
        out[:330, 390:, :] = 0
        
        # Clean stray pixels in left flank x < 187 above y=290
        out[:290, :187, :] = 0
            
        # In the collar zone (x in [195..285]), fill collar socket down to y=276
        for x in range(195, 286):
            norm_x = (x - 240.0) / 45.0
            if abs(norm_x) <= 1.0:
                top_cy = 276.0 - 12.0 * np.sqrt(1.0 - norm_x**2)
                y_start = int(round(top_cy))
                for y in range(y_start, 278):
                    dist = y - top_cy
                    if dist <= 1.8:
                        out[y, x] = rim_dark
                    elif dist <= 3.8:
                        out[y, x] = metal_bright
                    elif dist <= 6.0:
                        out[y, x] = metal_mid
                    else:
                        out[y, x] = socket_dark
                        
        # Smooth continuous dark outer rim line along the collar curve
        for x in range(194, 287):
            norm_x = (x - 240.0) / 45.0
            if abs(norm_x) <= 1.0:
                top_cy = int(round(276.0 - 12.0 * np.sqrt(1.0 - norm_x**2)))
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
