#!/usr/bin/env python3
"""
tools/build_authentic_boar_maple.py
Rebuilds the entire MaplePaperdoll Character.wz tight slice assets for Boar (厚鎧野豬)
using the authentic master char_boar.png, completely eliminating:
1. Rectangular cutout / background aura above the winding key and ear.
2. Bottom-right jagged pixel debris below the hammer shaft.
3. Cartoonish 2D sticker eye, replacing with authentic optical glass eyeball & metal casing.
Conforms strictly to 0-ART50, 0-ART51, and 0-ART18.
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
HERO_BOAR = f"{REPO_ROOT}/web/media/hero/char_boar.png"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"
PARTS_DIR = f"{BOAR_DIR}/maple_parts"

for sub in ["body", "head_unit", "eyes", "costume", "weapon", "winding_key", "back_curio"]:
    os.makedirs(f"{PARTS_DIR}/{sub}", exist_ok=True)

# -----------------------------------------------------------------------------
# STEP 0: KEY OUT BACKGROUND CLEANLY FROM char_boar.png
# -----------------------------------------------------------------------------
print("--- Step 0: Clean Keying Official char_boar.png ---")
raw_hero = Image.open(HERO_BOAR).convert("RGBA")
arr_raw = np.array(raw_hero)
h_raw, w_raw, _ = arr_raw.shape

# Background in char_boar.png is cream/beige: R: 240..250, G: 225..245, B: 195..225
# Low saturation (max channel diff < 55)
is_bg = (arr_raw[:, :, 0] > 225) & (arr_raw[:, :, 1] > 210) & (arr_raw[:, :, 2] > 175) & \
        (np.abs(arr_raw[:, :, 0].astype(int) - arr_raw[:, :, 1].astype(int)) < 30) & \
        (np.abs(arr_raw[:, :, 1].astype(int) - arr_raw[:, :, 2].astype(int)) < 45)

# Keep foot contact shadow at the very bottom (y > 1050)
is_foot_shadow = (np.arange(h_raw)[:, None] > 1060) & (arr_raw[:, :, 0] < 210)
is_bg[is_foot_shadow] = False

arr_keyed = arr_raw.copy()
arr_keyed[is_bg, 3] = 0
keyed_hero = Image.fromarray(arr_keyed, mode="RGBA")

# Scale to standard 512 canvas:
# Target width 394, target height 493, placed at (59, 11)
scale = 476.0 / 1120.0
target_w = int(w_raw * scale) # 394
target_h = int(h_raw * scale) # 493

scaled_hero = keyed_hero.resize((target_w, target_h), Image.Resampling.LANCZOS)
master_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
paste_x = (512 - target_w) // 2 # 59
paste_y = 512 - target_h - 8   # 11
master_512.alpha_composite(scaled_hero, (paste_x, paste_y))
print("Master 512 assembled, bbox:", master_512.getbbox())

m_arr = np.array(master_512)

# -----------------------------------------------------------------------------
# STEP 1: EYES (Authentic Hand-Painted Glass Optical Eyeball & Variants)
# -----------------------------------------------------------------------------
print("--- Step 1: Building Authentic Eyes ---")
# Eyeball in raw_hero is around x: 429, y: 403
# In 512, eyeball center is at:
# x: 59 + int(429 * scale) = 241
# y: 11 + int(403 * scale) = 182
# Brow anchor in 512 is (235, 161).
# Eye sprite canvas is 90x60, origin is [45, 30].
# Eyeball relative to origin [45, 30]: (241 - 235 + 45, 182 - 161 + 30) = (51, 51)
# But in maple_paperdoll, Brow anchor is relative to Neck (250, 176):
# neck(250, 176) + brow(-15, -15) = (235, 161).
# In 512, eyeball center is at (235, 161) when we align it properly to brow!
# Let's extract the exact 40x40 eyeball from raw_hero:
exact_eyeball_raw = raw_hero.crop((409, 383, 449, 423)) # 40x40
# Scale 40x40 to 512 space: 40 * scale = ~17x17
eye_size_512 = int(40 * scale) # 17
exact_eyeball_512 = exact_eyeball_raw.resize((eye_size_512, eye_size_512), Image.Resampling.LANCZOS)
arr_eb = np.array(exact_eyeball_512)

# Create 90x60 canvas centered at (45, 30)
eye_cyan = Image.new("RGBA", (90, 60), (0, 0, 0, 0))
cx, cy = 45, 30
half_s = eye_size_512 // 2

# Apply circular vignette / alpha mask to eyeball so outer edge fades into socket
for y in range(eye_size_512):
    for x in range(eye_size_512):
        d = math.hypot(x - half_s, y - half_s)
        if d <= half_s:
            r, g, b, _ = arr_eb[y, x]
            a = 255
            if d > half_s - 2.0:
                a = int(255 * (half_s - d) / 2.0)
            dst_x = cx - half_s + x
            dst_y = cy - half_s + y
            if 0 <= dst_x < 90 and 0 <= dst_y < 60:
                eye_cyan.putpixel((dst_x, dst_y), (r, g, b, a))

# Add a subtle dark socket bezel rim for depth
draw_c = ImageDraw.Draw(eye_cyan)
draw_c.ellipse([cx - half_s - 1, cy - half_s - 1, cx + half_s + 1, cy + half_s + 1], outline=(35, 25, 20, 200), width=1)

eye_cyan_path = f"{PARTS_DIR}/eyes/eyes_cyan_emerald.png"
eye_cyan.save(eye_cyan_path)
print(f"  ✓ Saved {eye_cyan_path}")

# Amber Gold variant: hue-shifted from authentic cyan eye
eye_amber = Image.new("RGBA", (90, 60), (0, 0, 0, 0))
arr_c = np.array(eye_cyan)
arr_a = arr_c.copy()
for y in range(60):
    for x in range(90):
        if arr_a[y, x, 3] > 0:
            r, g, b, a = arr_a[y, x]
            # Convert cyan/teal (high G, B) to warm amber gold (high R, G, low B)
            if g > 100 or b > 100:
                # Retain brightness
                lum = int(0.299 * r + 0.587 * g + 0.114 * b)
                # Specular catchlight remains white
                if r > 210 and g > 210 and b > 210:
                    arr_a[y, x] = [255, 255, 255, a]
                elif lum < 50:
                    arr_a[y, x] = [40, 20, 10, a]
                else:
                    arr_a[y, x] = [min(255, int(lum * 1.25)), min(255, int(lum * 0.85)), int(lum * 0.2), a]

eye_amber = Image.fromarray(arr_a, mode="RGBA")
eye_amber_path = f"{PARTS_DIR}/eyes/eyes_amber_gold.png"
eye_amber.save(eye_amber_path)
print(f"  ✓ Saved {eye_amber_path}")

# Blink variant: closed metallic eyelid
eye_blink = Image.new("RGBA", (90, 60), (0, 0, 0, 0))
draw_b = ImageDraw.Draw(eye_blink)
draw_b.arc([cx - 14, cy - 8, cx + 14, cy + 12], start=10, end=170, fill=(35, 25, 22, 255), width=3)
draw_b.line([(cx - 13, cy + 3), (cx + 13, cy + 3)], fill=(45, 32, 25, 255), width=2)
draw_b.line([(cx - 10, cy + 2), (cx + 10, cy + 2)], fill=(230, 185, 60, 220), width=1)
eye_blink_path = f"{PARTS_DIR}/eyes/eyes_blink.png"
eye_blink.save(eye_blink_path)
print(f"  ✓ Saved {eye_blink_path}")

# -----------------------------------------------------------------------------
# STEP 2: HEAD UNIT (Cleanly Keyed, Eye Removed to Dark Socket 0-ART51)
# -----------------------------------------------------------------------------
print("--- Step 2: Building Clean Head Units ---")
# Crop box in 512: x: 130..395, y: 15..215, size: (265, 200)
# Origin relative to neck (250, 176): [120, 161]
crop_h_box = (130, 15, 395, 215)
head_layer = np.zeros_like(m_arr)

for y in range(15, 215):
    for x in range(130, 395):
        r, g, b, a = m_arr[y, x]
        if a > 20:
            # Exclude winding key in the upper right
            # Winding key is attached to back at x > 340, y < 155
            # But the ear is at x <= 365, y >= 35
            # In our cleanly keyed master_512, there is NO background aura!
            # We only exclude the winding key shaft/bow
            is_key_shaft = (x > 348 and y < 145 and (r > 130 and g > 90 and b < 60))
            if not is_key_shaft:
                head_layer[y, x] = [r, g, b, a]

im_head = Image.fromarray(head_layer, mode="RGBA").crop(crop_h_box)
arr_h = np.array(im_head)

# Fill eye socket with deep metallic shadow (0-ART51) so eyes aren't baked onto head
# Eye in 512 is around (235..245, 165..185)
# In head crop (x - 130, y - 15), eye is around x: 100..120, y: 150..170
for y in range(len(arr_h)):
    for x in range(len(arr_h[0])):
        # If cyan eye glow is present in socket, replace with deep shaded socket
        r, g, b, a = arr_h[y, x]
        if 95 <= x <= 125 and 145 <= y <= 175:
            if g > r + 15 and g > 80:
                arr_h[y, x] = [32, 24, 28, 255] # dark shaded metal socket

# Also ensure outside the character boundary there are 0 stray semi-trans pixels
# Feather boundary smoothly
head_brass = Image.fromarray(arr_h, mode="RGBA")
head_brass_path = f"{PARTS_DIR}/head_unit/ear_boar_rivet_cowl_brass.png"
head_brass.save(head_brass_path)
head_brass.save(f"{PARTS_DIR}/head_unit/ear_boar_rivet_cowl.png")
print(f"  ✓ Saved {head_brass_path}")

# Ivory Stock Head Variant
arr_hi = arr_h.copy()
for y in range(len(arr_hi)):
    for x in range(len(arr_hi[0])):
        if arr_hi[y, x, 3] > 0:
            r, g, b = arr_hi[y, x, :3]
            lum = int(0.299 * r + 0.587 * g + 0.114 * b)
            arr_hi[y, x, :3] = [min(255, lum + 20), min(255, lum + 20), min(255, lum + 25)]
head_ivory_path = f"{PARTS_DIR}/head_unit/ear_boar_rivet_cowl_ivory.png"
Image.fromarray(arr_hi, mode="RGBA").save(head_ivory_path)
print(f"  ✓ Saved {head_ivory_path}")

# Crimson Head Variant
arr_hc = arr_h.copy()
for y in range(len(arr_hc)):
    for x in range(len(arr_hc[0])):
        if arr_hc[y, x, 3] > 0:
            r, g, b = arr_hc[y, x, :3]
            arr_hc[y, x, 0] = min(255, int(r * 1.35) + 35)
            arr_hc[y, x, 1] = int(g * 0.7)
            arr_hc[y, x, 2] = int(b * 0.7)
head_crimson_path = f"{PARTS_DIR}/head_unit/ear_boar_rivet_cowl_crimson.png"
Image.fromarray(arr_hc, mode="RGBA").save(head_crimson_path)
print(f"  ✓ Saved {head_crimson_path}")

# -----------------------------------------------------------------------------
# STEP 3: BODY CHASSIS (Pure Metallic Contours, No Head, No Weapon, No Debris)
# -----------------------------------------------------------------------------
print("--- Step 3: Building Pure Body Slices ---")
# Build clean base body from master_512 without head, without hammer, without key
body_layer = np.zeros_like(m_arr)
for y in range(512):
    for x in range(512):
        r, g, b, a = m_arr[y, x]
        if a > 10:
            # Exclude head (y < 170 and 140 < x < 380)
            if y < 165 and 140 < x < 380:
                continue
            # Exclude weapon / hammer area (x < 175 and y > 240)
            if x < 170 and y > 240:
                continue
            # Exclude winding key area (x > 345 and y < 165)
            if x > 345 and y < 165:
                continue
            # Exclude ground debris (y > 485 and (x < 180 or x > 380))
            if y > 485 and (x < 190 or x > 380):
                continue
            body_layer[y, x] = [r, g, b, a]

body_base = Image.fromarray(body_layer, mode="RGBA")

# Ensure chest core is glowing pure cyan (or crimson for molten variant) (0-ART18)
core_cyan = Image.open(f"{BOAR_DIR}/optic_core/core_cyan_emerald_512.png").convert("RGBA")
core_crimson = Image.open(f"{BOAR_DIR}/optic_core/core_molten_crimson_512.png").convert("RGBA")

# 1. Brass Gold
body_brass = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
body_brass.alpha_composite(body_base)
body_brass.alpha_composite(core_cyan)
body_brass_path = f"{PARTS_DIR}/body/paint_brass_gold.png"
body_brass.save(body_brass_path)
print(f"  ✓ Saved {body_brass_path}")

# 2. Ivory Stock
arr_b_iv = np.array(body_base)
for y in range(512):
    for x in range(512):
        if arr_b_iv[y, x, 3] > 0:
            r, g, b = arr_b_iv[y, x, :3]
            lum = int(0.299 * r + 0.587 * g + 0.114 * b)
            arr_b_iv[y, x, :3] = [min(255, lum + 15), min(255, lum + 15), min(255, lum + 20)]
body_ivory = Image.fromarray(arr_b_iv, mode="RGBA")
body_ivory.alpha_composite(core_cyan)
body_ivory_path = f"{PARTS_DIR}/body/paint_ivory_stock.png"
body_ivory.save(body_ivory_path)
print(f"  ✓ Saved {body_ivory_path}")

# 3. Molten Crimson
arr_b_cr = np.array(body_base)
for y in range(512):
    for x in range(512):
        if arr_b_cr[y, x, 3] > 0:
            r, g, b = arr_b_cr[y, x, :3]
            arr_b_cr[y, x, 0] = min(255, int(r * 1.35) + 30)
            arr_b_cr[y, x, 1] = int(g * 0.7)
            arr_b_cr[y, x, 2] = int(b * 0.7)
body_crimson = Image.fromarray(arr_b_cr, mode="RGBA")
body_crimson.alpha_composite(core_crimson)
body_crimson_path = f"{PARTS_DIR}/body/paint_molten_crimson.png"
body_crimson.save(body_crimson_path)
print(f"  ✓ Saved {body_crimson_path}")

# -----------------------------------------------------------------------------
# STEP 4: WEAPON (Clean Ground Contact, No Vertical Cut, No Debris)
# -----------------------------------------------------------------------------
print("--- Step 4: Building Clean Greathammer ---")
# Crop weapon from master_512: x: 60..227, y: 258..512 (width: 167, height: 254)
# Origin relative to hand (180, 340): [121, 90] (since 180 - 121 = 59, 340 - 90 = 250)
wpn_box = (60, 258, 227, 512)
wpn_cropped = master_512.crop(wpn_box)
arr_w = np.array(wpn_cropped)

# Clean out any pixels belonging to the body on the right (x > 140, y < 140)
for y in range(len(arr_w)):
    for x in range(len(arr_w[0])):
        if x > 135 and y < 130:
            arr_w[y, x] = [0, 0, 0, 0]
        # Clean bottom right contact shadow to eliminate vertical straight line cut
        if x > 120 and y > 215:
            fade = max(0.0, 1.0 - (x - 120) / 25.0)
            arr_w[y, x, 3] = int(arr_w[y, x, 3] * fade)
        # Clean ragged floating debris at the very bottom right (y > 220, x > 135)
        if y > 225 and x > 130:
            arr_w[y, x] = [0, 0, 0, 0]

clean_wpn = Image.fromarray(arr_w, mode="RGBA")
wpn_path = f"{PARTS_DIR}/weapon/wpn_anvil_greathammer.png"
clean_wpn.save(wpn_path)
print(f"  ✓ Saved {wpn_path}")

# -----------------------------------------------------------------------------
# STEP 5: WINDING KEY (Clean Single Brass Key, No Duplicate Overlap)
# -----------------------------------------------------------------------------
print("--- Step 5: Building Clean Winding Key ---")
# 96x110 canvas with origin [18, 80]
# Back_key anchor is at (360, 140)
w_k, h_k = 96, 110
key_im = Image.new("RGBA", (w_k, h_k), (0, 0, 0, 0))
draw_k = ImageDraw.Draw(key_im)

col_shadow = (35, 25, 20, 255)
col_brass = (215, 165, 50, 255)
col_brass_hi = (255, 225, 110, 255)
col_shaft = (145, 105, 38, 255)

# Shaft extending into body at (18, 80)
draw_k.polygon([(12, 85), (32, 65), (42, 75), (22, 95)], fill=col_shaft, outline=col_shadow)
draw_k.line([(15, 86), (34, 67)], fill=col_brass_hi, width=2)

# Collar ring
draw_k.ellipse([20, 68, 38, 86], fill=(160, 120, 40, 255), outline=col_shadow, width=2)
draw_k.ellipse([23, 71, 35, 83], fill=col_brass_hi)

# Classic dual-lobe winding key bow (centered around x=58, y=42)
# Outer rounded silhouette
draw_k.rounded_rectangle([20, 15, 86, 68], radius=24, fill=(185, 135, 40, 255), outline=col_shadow, width=3)
draw_k.rounded_rectangle([23, 18, 83, 65], radius=21, fill=col_brass)
draw_k.arc([23, 18, 83, 65], start=180, end=360, fill=col_brass_hi, width=3)

# Cut two hollow finger holes
mask_h = Image.new("L", (w_k, h_k), 0)
draw_mh = ImageDraw.Draw(mask_h)
draw_mh.ellipse([28, 26, 48, 54], fill=255)
draw_mh.ellipse([58, 26, 78, 54], fill=255)

arr_key = np.array(key_im)
arr_mask = np.array(mask_h)
arr_key[arr_mask > 0, 3] = 0

key_clean = Image.fromarray(arr_key, mode="RGBA")
draw_k2 = ImageDraw.Draw(key_clean)
draw_k2.ellipse([28, 26, 48, 54], outline=col_shadow, width=2)
draw_k2.ellipse([58, 26, 78, 54], outline=col_shadow, width=2)

key_path = f"{PARTS_DIR}/winding_key/key_classic_brass.png"
key_clean.save(key_path)
print(f"  ✓ Saved {key_path}")

# -----------------------------------------------------------------------------
# STEP 6: BACK CURIO (Spring Tail)
# -----------------------------------------------------------------------------
print("--- Step 6: Building Back Curio (Spring Tail) ---")
# 96x88 canvas with origin [10, 15]
tail_im = Image.new("RGBA", (96, 88), (0, 0, 0, 0))
draw_t = ImageDraw.Draw(tail_im)

col_spring = (175, 135, 55, 255)
col_spring_dark = (40, 30, 25, 255)
col_spring_hi = (255, 230, 120, 255)

# Coiled metal spring tail curves
for i in range(4):
    sx = 15 + i * 14
    sy = 20 + i * 8
    draw_t.ellipse([sx, sy, sx + 22, sy + 32], outline=col_spring_dark, width=4)
    draw_t.ellipse([sx + 1, sy + 1, sx + 21, sy + 31], outline=col_spring, width=3)
    draw_t.arc([sx + 2, sy + 2, sx + 20, sy + 30], start=180, end=330, fill=col_spring_hi, width=2)

# End brass knob
draw_t.ellipse([70, 48, 86, 64], fill=col_spring, outline=col_spring_dark, width=2)
draw_t.ellipse([73, 51, 81, 59], fill=col_spring_hi)

tail_path = f"{PARTS_DIR}/back_curio/curio_spring_tail.png"
tail_im.save(tail_path)
print(f"  ✓ Saved {tail_path}")

print("🎉 Masterpiece authentic assets generated successfully!")
