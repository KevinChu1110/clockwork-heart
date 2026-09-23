#!/usr/bin/env python3
"""
build_tortoise_slices.py (v5 - Production Master)
Definitive production script for The Xuanji Tortoise (玄機龜, 10th Race) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/XUANJI_TORTOISE_DESIGN_PROPOSAL.md
- docs/world/CANON.md
- art_direction.md 15-item checklist
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART27, 0-ART28, 0-ART28r
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
TORTOISE_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/tortoise"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon & Dopamine Color Palette
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple outline
JADE_PRIMARY = (45, 106, 79, 255)      # #2D6A4F Jade Bronze Primary
JADE_DARK = (28, 68, 50, 255)
JADE_LIGHT = (72, 160, 120, 255)
JADE_SHINE = (110, 210, 160, 255)

WHITE_PLATE = (255, 253, 248, 255)     # #FFFDF8 Marble cream white
WHITE_SHINE = (255, 255, 255, 255)
WHITE_SHADOW = (220, 215, 205, 255)

BRASS_GOLD = (255, 208, 40, 255)       # #FFD028 Tianyuan Brass Gold
BRASS_DARK = (180, 130, 20, 255)
BRASS_DEEP = (110, 75, 15, 255)
BRASS_LIGHT = (255, 235, 120, 255)

AMBER_CORE = (255, 160, 16, 255)       # #FFA010 Amber Quartz Lens
AMBER_LIGHT = (255, 215, 80, 255)
AMBER_DARK = (180, 90, 10, 255)

EMERALD_MINT = (78, 216, 106, 255)     # #4ED86A Mint Emerald Core
EMERALD_LIGHT = (150, 250, 175, 255)
EMERALD_DARK = (30, 130, 55, 255)

def build_all_slices():
    print("=== BUILDING THE XUANJI TORTOISE 7 PAPERDOLL SLICES (V5 FINAL) ===")
    
    # 1. Base image from /tmp/tortoise_main_view.png
    src_path = "/tmp/tortoise_main_view.png"
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Missing {src_path}")
    
    raw = Image.open(src_path).convert("RGB")
    arr = np.array(raw)
    r = arr[:, :, 0].astype(int)
    g = arr[:, :, 1].astype(int)
    b = arr[:, :, 2].astype(int)
    
    # Clean chroma key (no magenta residue)
    is_magenta_bg = (r > 200) & (b > 200) & (g < 70)
    is_edge = (r > 180) & (b > 180) & (g < 95) & (~is_magenta_bg)
    
    rgba = np.zeros((arr.shape[0], arr.shape[1], 4), dtype=np.uint8)
    rgba[:, :, :3] = arr
    rgba[:, :, 3] = 255
    rgba[is_magenta_bg, 3] = 0
    rgba[is_edge, 3] = 120
    rgba[:, 820:, 3] = 0 # Crop secondary view
    
    clean_im = Image.fromarray(rgba)
    bbox = clean_im.getbbox()
    print("  ✓ Perfectly isolated character bbox:", bbox)
    cropped = clean_im.crop(bbox)
    
    # Save concept art
    docs_art_path = f"{REPO_ROOT}/docs/art/xuanji_tortoise_concept.png"
    cropped.save(docs_art_path)
    print(f"  ✓ Saved clean concept art to {docs_art_path}")

    # Scale to 128x128
    # Feet at y=114, head top around y=32, target height 82px
    target_h = 82
    scale = target_h / cropped.height
    target_w = int(cropped.width * scale)
    scaled = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    master_128 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = 64 - target_w // 2
    py = 114 - target_h
    master_128.paste(scaled, (px, py), scaled)
    print(f"  ✓ Aligned master to 128x128 at pos ({px}, {py}), bbox:", master_128.getbbox())

    # Prepare directories
    for sub in ["chassis", "head_unit", "winding_key", "costume", "optic_core", "weapon", "back_curio"]:
        os.makedirs(f"{TORTOISE_PD_DIR}/{sub}", exist_ok=True)
    os.makedirs(KEY_DIR, exist_ok=True)
    os.makedirs(WEAPON_DIR, exist_ok=True)

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5)
    # File: winding_key/key_tai_chi_dual_fish.png
    # Location: Upper back on left (x: 20..46, y: 16..46)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(14, 48):
        for x in range(18, 48):
            raw_p = master_128.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4: continue
            r_v, g_v, b_v, a_v = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a_v < 25: continue
            
            # Tai Chi dual fish brass key pixels (x <= 40 or y <= 35)
            if x <= 40 or y <= 35:
                key_img.putpixel((x, y), (r_v, g_v, b_v, a_v))

    kd = ImageDraw.Draw(key_img)
    # Key stem entering shell
    kd.line([(34, 35), (39, 42)], fill=BRASS_DEEP, width=3)
    kd.line([(35, 34), (40, 41)], fill=BRASS_GOLD, width=2)
    kd.line([(36, 33), (41, 40)], fill=BRASS_LIGHT, width=1)
    print("  ✓ Slice 1 Winding Key built, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8)
    # File: back_curio/curio_bagua_armillary_rings.png
    # Tail rudder & back balance bracket (x: 24..38, y: 95..115)
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)
    
    # Grounded three-stage hinge tail rudder and balance bracket
    for y in range(95, 115):
        for x in range(24, 40):
            raw_p = master_128.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4: continue
            r_v, g_v, b_v, a_v = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a_v < 30: continue
            if x <= 33:
                curio_img.putpixel((x, y), (r_v, g_v, b_v, a_v))
                
    # Brass mini tail rudder coupler
    cd.ellipse([27, 102, 33, 108], fill=BRASS_GOLD, outline=OUTLINE, width=1)
    cd.point((29, 104), fill=WHITE_SHINE)
    print("  ✓ Slice 2 Back Curio built, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10)
    # File: chassis/paint_tortoise_jade.png
    # Complete torso base, carapace back, legs, footpads, contact shadow
    # Four feet firmly planted on soft contact shadow (no floating gap!)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow: tight under feet (x: 28..100, y: 110..118)
    # Center x=64, y=114, radius_x=34, radius_y=4
    ch_d.ellipse([64 - 34, 114 - 4, 64 + 34, 114 + 4], fill=(31, 26, 58, 120))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.4))

    # 2. Extract character torso, legs, claws, shell from master
    for y in range(H):
        for x in range(W):
            raw_p = master_128.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4: continue
            r_v, g_v, b_v, a_v = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a_v < 25: continue

            # Exclude weapon on the right: x >= 74 and y <= 84
            if x >= 74 and y <= 84: continue
            # Exclude winding key on top-left: x <= 40 and y <= 35
            if x <= 40 and y <= 35: continue
            # Exclude head shell: y <= 50 and 44 <= x <= 86
            if y <= 50 and 44 <= x <= 86: continue

            chassis_img.putpixel((x, y), (r_v, g_v, b_v, a_v))

    print("  ✓ Slice 3 Chassis built, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_xuanji_tortoise_stock.png
    # Cranial helmet shell, neck sleeve, jaws (x: 42..88, y: 20..58)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(20, 58):
        for x in range(42, 88):
            raw_p = master_128.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4: continue
            r_v, g_v, b_v, a_v = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a_v < 25: continue
            
            # Exclude key on left
            if x <= 40 and y <= 35: continue
            # Exclude amber eye lens (reserved for optic_core)
            is_eye = (52 <= x <= 78 and 36 <= y <= 48 and r_v > 160 and g_v > 110 and b_v < 80)
            if is_eye: continue

            head_img.putpixel((x, y), (r_v, g_v, b_v, a_v))

    hd = ImageDraw.Draw(head_img)
    # Helmet ridge highlight
    hd.line([(62, 24), (66, 30)], fill=JADE_SHINE, width=1)
    print("  ✓ Slice 4 Head Unit built, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (Z: 25)
    # File: costume/costume_zen_dojo_harness.png
    # Dojo harness plates, pauldrons, waist harness (x: 44..84, y: 52..96)
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(52, 96):
        for x in range(44, 84):
            raw_p = master_128.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4: continue
            r_v, g_v, b_v, a_v = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a_v < 30: continue
            
            # Exclude glowing heart gem in chest
            if 58 <= x <= 68 and 64 <= y <= 76 and (g_v > 170 and r_v < 130): continue

            costume_img.putpixel((x, y), (r_v, g_v, b_v, a_v))

    cos_d = ImageDraw.Draw(costume_img)
    # Zen Dojo belt buckle
    cos_d.rectangle([59, 78, 67, 84], outline=OUTLINE, fill=BRASS_GOLD)
    cos_d.rectangle([61, 80, 65, 82], fill=BRASS_DARK)
    print("  ✓ Slice 5 Costume built, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30)
    # File: optic_core/core_amber_quartz.png
    # Amber quartz optical eyes & glowing mint emerald heart gem
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(35, 50):
        for x in range(50, 80):
            raw_p = master_128.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4: continue
            r_v, g_v, b_v, a_v = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a_v < 25: continue
            if (52 <= x <= 76 and 36 <= y <= 48) and (r_v > 110 or g_v > 75):
                core_img.putpixel((x, y), (r_v, g_v, b_v, a_v))

    for y in range(64, 76):
        for x in range(56, 70):
            raw_p = master_128.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4: continue
            r_v, g_v, b_v, a_v = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a_v < 25: continue
            if g_v > 120 or (r_v > 140 and g_v > 140 and b_v > 140):
                core_img.putpixel((x, y), (r_v, g_v, b_v, a_v))

    cord = ImageDraw.Draw(core_img)
    # Catchlight points
    cord.point((58, 41), fill=WHITE_SHINE)
    cord.point((70, 41), fill=WHITE_SHINE)
    # Heart specular
    cord.line([(63, 67), (63, 73)], fill=WHITE_SHINE, width=1)
    print("  ✓ Slice 6 Optic Core built, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/wpn_bagua_astrolabe.png
    # Xuanji Bagua Astrolabe / Bulwark Float-Crystal (x: 74..104, y: 36..92)
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(36, 92):
        for x in range(74, 110):
            raw_p = master_128.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4: continue
            r_v, g_v, b_v, a_v = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a_v < 25: continue
            weapon_img.putpixel((x, y), (r_v, g_v, b_v, a_v))

    print("  ✓ Slice 7 Weapon built, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 and 512x512)
    # ─────────────────────────────────────────────────────────────
    slices = [
        ("chassis", "paint_tortoise_jade", chassis_img),
        ("head_unit", "head_xuanji_tortoise_stock", head_img),
        ("winding_key", "key_tai_chi_dual_fish", key_img),
        ("costume", "costume_zen_dojo_harness", costume_img),
        ("optic_core", "core_amber_quartz", core_img),
        ("weapon", "wpn_bagua_astrolabe", weapon_img),
        ("back_curio", "curio_bagua_armillary_rings", curio_img)
    ]

    for slot, item_id, img in slices:
        dst_128 = f"{TORTOISE_PD_DIR}/{slot}/{item_id}.png"
        img.save(dst_128)
        img_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
        dst_512 = f"{TORTOISE_PD_DIR}/{slot}/{item_id}_512.png"
        img_512.save(dst_512)

    # Universal copies
    shutil.copyfile(f"{TORTOISE_PD_DIR}/winding_key/key_tai_chi_dual_fish.png", f"{KEY_DIR}/key_tai_chi_dual_fish.png")
    shutil.copyfile(f"{TORTOISE_PD_DIR}/weapon/wpn_bagua_astrolabe.png", f"{WEAPON_DIR}/wpn_bagua_astrolabe.png")
    print("  ✓ Slices saved to 128x128 and 512x512, universal copies synchronized")

    # ─────────────────────────────────────────────────────────────
    # GENERATE PROOFS
    # ─────────────────────────────────────────────────────────────
    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    composite.alpha_composite(key_img)
    composite.alpha_composite(curio_img)
    composite.alpha_composite(chassis_img)
    composite.alpha_composite(head_img)
    composite.alpha_composite(costume_img)
    composite.alpha_composite(core_img)
    composite.alpha_composite(weapon_img)

    proof_comp = f"{TORTOISE_PD_DIR}/proof_paperdoll_tortoise_composite.png"
    composite.save(proof_comp)

    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{TORTOISE_PD_DIR}/proof_paperdoll_tortoise_magenta.png"
    magenta_bg.save(proof_mag)

    strip_w = W * 7 + 8 * 8
    strip_h = H + 24
    strip_img = Image.new("RGBA", (strip_w, strip_h), (24, 20, 36, 255))
    sd = ImageDraw.Draw(strip_img)

    titles = ["Key (Z:5)", "Curio (Z:8)", "Chassis (Z:10)", "Head (Z:20)", "Costume (Z:25)", "Core (Z:30)", "Weapon (Z:40)"]
    imgs = [key_img, curio_img, chassis_img, head_img, costume_img, core_img, weapon_img]

    for i, (t, simg) in enumerate(zip(titles, imgs)):
        sx = 8 + i * (W + 8)
        sy = 16
        cb = Image.new("RGBA", (W, H), (45, 40, 60, 255))
        cb_d = ImageDraw.Draw(cb)
        for cy in range(0, H, 16):
            for cx in range(0, W, 16):
                if (cx // 16 + cy // 16) % 2 == 1:
                    cb_d.rectangle([cx, cy, cx + 15, cy + 15], fill=(55, 50, 75, 255))
        cb.alpha_composite(simg)
        strip_img.paste(cb, (sx, sy))
        sd.text((sx + 4, 2), t, fill=(255, 208, 40, 255))

    proof_7 = f"{TORTOISE_PD_DIR}/proof_tortoise_all_7_slices.png"
    strip_img.save(proof_7)
    print("  ✓ Proof images regenerated")

if __name__ == "__main__":
    build_all_slices()
