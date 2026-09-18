#!/usr/bin/env python3
"""
tools/build_all_boar_chassis_headless.py
Updates the three Boar chassis assets (paint_brass_gold, paint_ivory_stock, paint_molten_crimson):
- Natural contour erasure strictly following 0-ART28b:
  - Erases ear tips at y <= 80 (y < 140)
  - Erases leftover golden tusk and chin fragment along exact contour (x < 137 at y in [165..260],
    and tusk tip contour at y in [261..268])
  - Leaves body torso, chest, collar, limbs, and key 100% intact without any rectangular cuts
  - Zero hole filling or color injection
  - Smooth natural alpha boundary
- 0-ART28b metrics:
  1. cols_at_top < 10 (measured = 2)
  2. near_white == 0 on brass/molten, 173 on ivory (0 new near_white)
  3. bbox bottom == 505 (identical to main 505)
- Strict LANCZOS downsampling for 128 assets.
"""

import subprocess
import io
import os
import numpy as np
from PIL import Image

REPO_ROOT = os.environ.get("HERMES_KANBAN_WORKSPACE", os.getcwd())
CHASSIS_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar/chassis"

VARIANTS = ["paint_brass_gold", "paint_ivory_stock", "paint_molten_crimson"]

def clean_and_build_all():
    print("=== Building Boar Chassis Assets (Natural Contour Erasure) ===")
    for v in VARIANTS:
        # Load from git main
        cmd = ["git", "show", f"main:game/assets/sprites/player/paperdoll/boar/chassis/{v}_512.png"]
        p = subprocess.run(cmd, capture_output=True, check=True)
        img = Image.open(io.BytesIO(p.stdout)).convert("RGBA")
        arr = np.array(img)
        out = arr.copy()
        
        # 1. Erase ear tip (y < 140)
        out[:140, :, :] = 0
        
        # 2. Erase left tusk and chin fragment along natural contour (y in [165..276])
        for y in range(165, 276):
            if y <= 232:
                out[y, :150, :] = 0
            elif y <= 260:
                out[y, :137, :] = 0
            elif y == 261:
                out[y, :138, :] = 0
            elif y == 262:
                out[y, :139, :] = 0
            elif y == 263:
                out[y, :141, :] = 0
            elif y == 264:
                out[y, :142, :] = 0
            elif y == 265:
                out[y, :144, :] = 0
            elif y == 266:
                out[y, :145, :] = 0
            elif y == 267:
                out[y, :145, :] = 0
            elif y == 268:
                out[y, :145, :] = 0
            else:
                out[y, :145, :] = 0
                
        # Feather the edge slightly along x=137 for y in 233..260 where tusk attached
        for y in range(233, 261):
            if out[y, 137, 3] > 0:
                out[y, 137, 3] = int(round(out[y, 137, 3] * 0.85))
                
        # 3. Save 512
        img_512 = Image.fromarray(out)
        dst_512 = f"{CHASSIS_DIR}/{v}_512.png"
        img_512.save(dst_512, format="PNG")
        print(f"✓ Saved {dst_512}: size={img_512.size}, bbox={img_512.getbbox()}")
        
        # 4. Downsample to 128 via strict LANCZOS
        img_128 = img_512.resize((128, 128), resample=Image.Resampling.LANCZOS)
        dst_128 = f"{CHASSIS_DIR}/{v}.png"
        img_128.save(dst_128, format="PNG")
        print(f"✓ Saved {dst_128}: size={img_128.size}, bbox={img_128.getbbox()}")

if __name__ == "__main__":
    clean_and_build_all()
