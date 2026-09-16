#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
TIGER_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/tiger"
WEAPON_UNIV = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

def update_slices():
    print("=== UPDATING EMBER TIGER PAPERDOLL SLICES ===")
    
    # 1. Clean costume_ember_tunic.png (remove waist sword)
    costume_p = f"{TIGER_PD}/costume/costume_ember_tunic.png"
    costume = Image.open(costume_p).convert("RGBA")
    c_arr = np.array(costume)
    
    # Clean the diagonal sword running across waist / skirt (x=54..82, y=82..95)
    for y in range(82, 96):
        for x in range(54, 82):
            r, g, b, a = c_arr[y, x]
            if a > 20:
                max_c = max(r, g, b)
                min_c = min(r, g, b)
                sat = (max_c - min_c) / max(1, max_c)
                if (max_c > 75 and sat < 0.25) or (r > 160 and g > 160 and b > 160):
                    if y <= 84:
                        c_arr[y, x] = [48, 32, 42, 255]
                    else:
                        c_arr[y, x] = [185, 56, 24, 255]

    # Clean sword strap at (67..72, 72..81)
    for y in range(72, 82):
        for x in range(67, 72):
            r, g, b, a = c_arr[y, x]
            if a > 20:
                if abs(int(r) - int(g)) < 30 and g > 70 and b > 50 and r < 150:
                    c_arr[y, x] = [215, 75, 25, 255]
                    
    # Clean gold pixels at right corner (79..80, 87..89)
    for y in range(87, 90):
        for x in range(79, 81):
            if c_arr[y, x, 3] > 20:
                c_arr[y, x] = [185, 45, 16, 255]

    cleaned_costume = Image.fromarray(c_arr)
    cleaned_costume.save(costume_p)
    print(f"✓ Saved cleaned {costume_p}")

    # 2. Re-create wpn_twin_ember_sabers.png (both sabers in both hands)
    # Original weapon
    orig_wpn = Image.open(f"{TIGER_PD}/weapon/wpn_twin_ember_sabers.png").convert("RGBA")
    w_arr = np.array(orig_wpn)
    
    # Extract blade1 (gear saber) and blade2 (flame saber)
    blade1_img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    for y in range(46, 105):
        for x in range(74, 91):
            if w_arr[y, x, 3] > 0:
                blade1_img.putpixel((x, y), tuple(w_arr[y, x]))

    blade2_img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    for y in range(46, 105):
        for x in range(92, 112):
            if w_arr[y, x, 3] > 0:
                blade2_img.putpixel((x, y), tuple(w_arr[y, x]))

    # Main hand: blade2 aligned at (88, 76)
    ms_arr = np.array(blade2_img)
    # Trim handle at y > 89
    for y in range(90, 105):
        ms_arr[y, :, :] = 0
    # Clean pommel at y=88..89
    ms_arr[89, 97:103] = [215, 160, 50, 255]
    ms_arr[89, 98:102] = [255, 210, 80, 255]
    
    clean_main = Image.fromarray(ms_arr)
    # Shift left by 5px so hilt is centered at (88, 76)
    main_aligned = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    main_aligned.paste(clean_main, (-5, 0), clean_main)

    # Off hand: blade1 in reverse grip
    b1_box = blade1_img.getbbox()
    assert b1_box is not None
    b1_c = blade1_img.crop(b1_box)
    b1_rev = b1_c.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    scale_dagger = 46.0 / 58.0
    b1_scaled = b1_rev.resize((int(round(b1_rev.width * scale_dagger)), 46), Image.Resampling.LANCZOS)
    
    off_aligned = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    off_aligned.paste(b1_scaled, (38 - 6, 77 - 10), b1_scaled)

    # Composite dual weapon layer:
    dual_wpn = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    dual_wpn.alpha_composite(main_aligned)
    dual_wpn.alpha_composite(off_aligned)
    
    wpn_target1 = f"{TIGER_PD}/weapon/wpn_twin_ember_sabers.png"
    wpn_target2 = f"{WEAPON_UNIV}/wpn_twin_ember_sabers.png"
    dual_wpn.save(wpn_target1)
    dual_wpn.save(wpn_target2)
    print(f"✓ Saved dual weapon: {wpn_target1} (bbox: {dual_wpn.getbbox()})")
    print(f"✓ Saved dual weapon: {wpn_target2}")

    # Also update paperdoll composite proof images
    from produce_clean_tiger_slices import main as produce_proofs
    # produce_clean_tiger_slices updates proofs in TIGER_PD
    import subprocess
    subprocess.run(["python3", f"{REPO_ROOT}/tools/produce_clean_tiger_slices.py"], check=True)

if __name__ == "__main__":
    update_slices()
