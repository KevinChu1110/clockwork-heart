#!/usr/bin/env python3
"""
tools/build_all_macaque_chassis_headless.py
Updates Macaque chassis and head_unit assets:
1. Chassis: paint_ivory_stock and paint_bamboo_bronze (512 and 128)
   - Headless (neck down), smooth metallic collar socket
   - 0 ears, 0 head
   - 100% complete body, limbs, winding key, and tail
   - Zero costume baked in (0-ART26b)
2. Head Unit: ear_macaque_coaxial (512 and 128)
   - Full face restored: emerald eyes, highlights, faceplate, muzzle, smiling mouth
   - Vintage diving helmet dome and coaxial ears
   - Zero square holes, zero 90-degree cutouts (0-ART27)
   - Exactly 2 ears
3. LANCZOS downsampling for 128 assets
"""

import os
from collections import deque
import numpy as np
from PIL import Image

REPO_ROOT = os.environ.get("HERMES_KANBAN_WORKSPACE", os.getcwd())
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"
CHASSIS_DIR = f"{MACAQUE_DIR}/chassis"
HEAD_DIR = f"{MACAQUE_DIR}/head_unit"
PROOFS_DIR = f"{REPO_ROOT}/proofs"

def filter_components(alpha_mask, min_size=50):
    h, w = alpha_mask.shape
    visited = np.zeros((h, w), dtype=bool)
    keep_mask = np.zeros((h, w), dtype=bool)
    
    for y in range(h):
        for x in range(w):
            if alpha_mask[y, x] and not visited[y, x]:
                comp = []
                q = deque([(y, x)])
                visited[y, x] = True
                while q:
                    cy, cx = q.popleft()
                    comp.append((cy, cx))
                    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < h and 0 <= nx < w and alpha_mask[ny, nx] and not visited[ny, nx]:
                            visited[ny, nx] = True
                            q.append((ny, nx))
                if len(comp) >= min_size:
                    for cy, cx in comp:
                        keep_mask[cy, cx] = True
    return keep_mask

def clean_and_build_all():
    ivory_orig = Image.open(f"{PROOFS_DIR}/old_chassis_ivory_512.png").convert("RGBA")
    bamboo_orig = Image.open(f"{PROOFS_DIR}/old_chassis_bamboo_512.png").convert("RGBA")
    
    arr_ivory = np.array(ivory_orig)
    arr_bamboo = np.array(bamboo_orig)
    h, w, _ = arr_ivory.shape
    
    # ── 1. DEFINE CONTINUOUS HEAD SEAM ──
    y_head_seam = np.zeros(w, dtype=int)
    for x in range(w):
        if x < 98 or x > 356:
            y_head_seam[x] = 0
        elif x < 125:
            # Left ear bottom: curves smoothly
            y_head_seam[x] = 198
        elif x < 145:
            t = (x - 125.0) / 20.0
            y_head_seam[x] = int(round(198.0 + 32.0 * t))
        elif x < 165:
            t = (x - 145.0) / 20.0
            y_head_seam[x] = int(round(230.0 + 20.0 * t))
        elif x <= 275:
            # Chin follows natural rounded curve: center at x=224, rx=52
            norm_x = (x - 224.0) / 52.0
            chin_y = 263.0 - 5.0 * (norm_x**2)
            y_head_seam[x] = int(round(chin_y))
        elif x <= 295:
            t = (x - 275.0) / 20.0
            y_head_seam[x] = int(round(258.0 - 18.0 * t))
        elif x <= 315:
            t = (x - 295.0) / 20.0
            y_head_seam[x] = int(round(240.0 - 22.0 * t))
        elif x <= 335:
            t = (x - 315.0) / 20.0
            y_head_seam[x] = int(round(218.0 - 8.0 * t))
        else:
            # Right ear bottom curve
            y_head_seam[x] = 210

    # ── 2. BUILD MASTER HEAD UNIT ──
    head_arr = np.zeros_like(arr_ivory)
    for x in range(w):
        ys = y_head_seam[x]
        if ys > 0:
            head_arr[:ys, x, :] = arr_ivory[:ys, x, :]
            
    head_arr[:, :98, :] = 0
    head_arr[:, 357:, :] = 0
    head_arr[head_arr[:, :, 3] < 10] = 0
    
    # Filter head to keep only primary component
    head_mask = filter_components(head_arr[:, :, 3] > 0, min_size=500)
    head_arr[~head_mask] = 0
    
    img_head_512 = Image.fromarray(head_arr)
    head_512_path = f"{HEAD_DIR}/ear_macaque_coaxial_512.png"
    img_head_512.save(head_512_path, format="PNG")
    print(f"✓ Saved {head_512_path} (512x512)")
    
    img_head_128 = img_head_512.resize((128, 128), resample=Image.Resampling.LANCZOS)
    head_128_path = f"{HEAD_DIR}/ear_macaque_coaxial.png"
    img_head_128.save(head_128_path, format="PNG")
    print(f"✓ Saved {head_128_path} (128x128 via LANCZOS)")
    
    # ── 3. BUILD MASTER CHASSIS (Ivory & Bamboo) ──
    y_chassis = np.zeros(w, dtype=int)
    for x in range(w):
        if x < 125:
            y_chassis[x] = 315
        elif x < 145:
            t = (x - 125.0) / 20.0
            y_chassis[x] = int(round(305.0 - 20.0 * t))
        elif x < 165:
            t = (x - 145.0) / 20.0
            y_chassis[x] = int(round(285.0 - 25.0 * t))
        elif x <= 295:
            y_chassis[x] = y_head_seam[x]
        elif x <= 308:
            y_chassis[x] = y_head_seam[x]
        elif x <= 347:
            norm_k = (x - 325.0) / 18.0
            top_ky = 230.0 - 4.0 * np.sqrt(max(0.0, 1.0 - min(1.0, norm_k**2)))
            y_chassis[x] = int(round(top_ky))
        else:
            y_chassis[x] = 150
            
    variants = [
        ("paint_ivory_stock", arr_ivory),
        ("paint_bamboo_bronze", arr_bamboo)
    ]
    
    for var_name, orig_arr in variants:
        ch_arr = np.zeros_like(orig_arr)
        for x in range(w):
            yc = y_chassis[x]
            ch_arr[yc:, x, :] = orig_arr[yc:, x, :]
            
        ch_arr[ch_arr[:, :, 3] < 10] = 0
        
        # Filter chassis to keep components >= 50 pixels
        ch_mask = filter_components(ch_arr[:, :, 3] > 0, min_size=50)
        ch_arr[~ch_mask] = 0
        
        # Save 512
        ch_512_p = f"{CHASSIS_DIR}/{var_name}_512.png"
        img_ch_512 = Image.fromarray(ch_arr)
        img_ch_512.save(ch_512_p, format="PNG")
        print(f"✓ Saved {ch_512_p} (512x512)")
        
        # Save 128 via strict LANCZOS
        ch_128_p = f"{CHASSIS_DIR}/{var_name}.png"
        img_ch_128 = img_ch_512.resize((128, 128), resample=Image.Resampling.LANCZOS)
        img_ch_128.save(ch_128_p, format="PNG")
        print(f"✓ Saved {ch_128_p} (128x128 via LANCZOS)")
        
        comp_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        comp_512.paste(img_ch_512, (0, 0), img_ch_512)
        comp_512.paste(img_head_512, (0, 0), img_head_512)
        
        comp_128 = comp_512.resize((128, 128), resample=Image.Resampling.LANCZOS)
        
        if var_name == "paint_ivory_stock":
            comp_128.save(f"{MACAQUE_DIR}/proof_paperdoll_macaque_composite.png")
            print(f"✓ Updated {MACAQUE_DIR}/proof_paperdoll_macaque_composite.png")

if __name__ == "__main__":
    clean_and_build_all()
