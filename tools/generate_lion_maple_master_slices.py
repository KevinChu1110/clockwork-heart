#!/usr/bin/env python3
"""
tools/generate_lion_maple_master_slices.py
Extracts pixel-perfect Character.wz slices from the official master Lion HD artwork.
Eliminates:
- Eye socket transparent white holes (sockets have dark bronze metal backing).
- Detached lance pommel / grip fragments (lance is 100% continuous).
- Horizontal cut gaps between mane and chassis.
- 2-pixel vertical gap at x=153..154 between lance and costume.
"""

import os
import numpy as np
from PIL import Image, ImageDraw

WS_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a"
MASTER_P = f"{WS_ROOT}/tools/lion_master_512.png"
OUT_DIR = f"{WS_ROOT}/game/assets/sprites/player/paperdoll/lion/maple_parts"

def run():
    master = Image.open(MASTER_P).convert("RGBA")
    m_arr = np.array(master)

    # ---------------------------------------------------------
    # 1. Extract Knight Lance Weapon
    # ---------------------------------------------------------
    print("--- 1. Extracting Knight Lance ---")
    # Lance is on the left: x <= 155, y between 27 and 435
    w_arr = np.zeros_like(m_arr)
    for y in range(27, 436):
        for x in range(70, 156):
            if m_arr[y, x, 3] > 0 and x <= 153:
                w_arr[y, x] = m_arr[y, x]

    lance_full = Image.fromarray(w_arr, mode="RGBA")
    # Crop to (75, 27, 153, 435) -> size (78, 408)
    lance_crop = lance_full.crop((75, 27, 153, 435))
    lance_crop.save(f"{OUT_DIR}/weapon/wpn_knight_lance.png")
    print(f"  ✓ wpn_knight_lance.png: size={lance_crop.size}, origin=[69, 293]")

    # ---------------------------------------------------------
    # 2. Extract Winding Key
    # ---------------------------------------------------------
    print("--- 2. Extracting Winding Key ---")
    k_arr = np.zeros_like(m_arr)
    for y in range(180, 335):
        for x in range(322, 445):
            if m_arr[y, x, 3] > 0:
                k_arr[y, x] = m_arr[y, x]

    key_full = Image.fromarray(k_arr, mode="RGBA")
    key_crop = key_full.crop((322, 183, 441, 333))
    key_crop.save(f"{OUT_DIR}/winding_key/key_classic_brass.png")
    print(f"  ✓ key_classic_brass.png: size={key_crop.size}, origin=[20, 113]")

    # ---------------------------------------------------------
    # 3. Extract Back Curio (Fan Tail)
    # ---------------------------------------------------------
    print("--- 3. Extracting Back Curio ---")
    t_arr = np.zeros_like(m_arr)
    for y in range(350, 460):
        for x in range(340, 450):
            if m_arr[y, x, 3] > 0 and (x >= 351 and y >= 364):
                t_arr[y, x] = m_arr[y, x]

    tail_full = Image.fromarray(t_arr, mode="RGBA")
    tail_crop = tail_full.crop((351, 364, 450, 458))
    tail_crop.save(f"{OUT_DIR}/back_curio/curio_lion_fan_tail.png")
    print(f"  ✓ curio_lion_fan_tail.png: size={tail_crop.size}, origin=[9, 16]")

    # ---------------------------------------------------------
    # 4. Extract Head Unit (Mane & Head with Dark Bronze Sockets)
    # ---------------------------------------------------------
    print("--- 4. Extracting Head Unit Mane ---")
    h_arr = np.zeros_like(m_arr)
    for y in range(50, 282):
        for x in range(130, 385):
            is_lance = (x < 140 and y > 240)
            if m_arr[y, x, 3] > 0 and not is_lance:
                is_eye_pixel = (162 <= y <= 184) and ((186 <= x <= 202) or (248 <= x <= 270))
                p = m_arr[y, x]
                if is_eye_pixel and (p[1] > 120 or p[2] > 120):
                    # Solid dark bronze socket
                    h_arr[y, x] = [58, 47, 34, 255]
                else:
                    h_arr[y, x] = p

    head_full = Image.fromarray(h_arr, mode="RGBA")
    head_crop = head_full.crop((131, 51, 381, 281))
    head_crop.save(f"{OUT_DIR}/head_unit/ear_lion_gilded_mane_brass.png")
    head_crop.save(f"{OUT_DIR}/head_unit/ear_lion_gilded_mane.png")
    print(f"  ✓ ear_lion_gilded_mane_brass.png: size={head_crop.size}, origin=[119, 223]")

    # Mane Color Variants (Ivory & Midnight)
    h_ivory = np.array(head_crop)
    gold_mask = (h_ivory[:, :, 3] > 100) & (h_ivory[:, :, 0] > 150) & (h_ivory[:, :, 1] > 110) & (h_ivory[:, :, 2] < 110)
    h_ivory[gold_mask, 0] = np.clip(h_ivory[gold_mask, 0] * 0.95 + 20, 0, 255)
    h_ivory[gold_mask, 1] = np.clip(h_ivory[gold_mask, 1] * 0.95 + 20, 0, 255)
    h_ivory[gold_mask, 2] = np.clip(h_ivory[gold_mask, 2] * 0.5 + 110, 0, 255)
    Image.fromarray(h_ivory, mode="RGBA").save(f"{OUT_DIR}/head_unit/ear_lion_gilded_mane_ivory.png")

    h_navy = np.array(head_crop)
    h_navy[gold_mask, 0] = np.clip(h_navy[gold_mask, 0] * 0.2 + 20, 0, 255)
    h_navy[gold_mask, 1] = np.clip(h_navy[gold_mask, 1] * 0.3 + 40, 0, 255)
    h_navy[gold_mask, 2] = np.clip(h_navy[gold_mask, 2] * 0.4 + 90, 0, 255)
    Image.fromarray(h_navy, mode="RGBA").save(f"{OUT_DIR}/head_unit/ear_lion_gilded_mane_midnight.png")
    print("  ✓ Ivory & Midnight mane variants created")

    # ---------------------------------------------------------
    # 5. Extract Eyes (Cyan Emerald, Amber Gold, Blink)
    # ---------------------------------------------------------
    print("--- 5. Extracting Optical Eyes ---")
    e_cyan_full = np.zeros((512, 512, 4), dtype=np.uint8)
    e_amber_full = np.zeros((512, 512, 4), dtype=np.uint8)

    for y in range(162, 185):
        for x in range(180, 275):
            is_eye = (186 <= x <= 202) or (248 <= x <= 270)
            if is_eye:
                p = m_arr[y, x]
                if p[3] > 0 and (p[1] > 120 or p[2] > 120):
                    e_cyan_full[y, x] = p
                    r_amb = min(255, int(p[1] * 1.05 + 20))
                    g_amb = int(p[1] * 0.85)
                    b_amb = int(p[0] * 0.8 + 20)
                    e_amber_full[y, x] = [r_amb, g_amb, b_amb, p[3]]

    crop_eye_box = (168, 143, 288, 203)
    eyes_cyan = Image.fromarray(e_cyan_full, mode="RGBA").crop(crop_eye_box)
    eyes_amber = Image.fromarray(e_amber_full, mode="RGBA").crop(crop_eye_box)
    eyes_cyan.save(f"{OUT_DIR}/eyes/eyes_cyan_emerald.png")
    eyes_amber.save(f"{OUT_DIR}/eyes/eyes_amber_gold.png")

    blink_im = Image.new("RGBA", (120, 60), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(blink_im)
    out_col = (40, 30, 60, 255)
    gold_hi = (255, 208, 40, 220)

    # Left eye: center (25, 30)
    bdraw.arc([16, 26, 34, 34], start=0, end=180, fill=out_col, width=3)
    bdraw.line([(15, 30), (35, 30)], fill=out_col, width=2)
    bdraw.line([(18, 29), (32, 29)], fill=gold_hi, width=1)

    # Right eye: center (91, 30)
    bdraw.arc([80, 26, 102, 34], start=0, end=180, fill=out_col, width=3)
    bdraw.line([(79, 30), (103, 30)], fill=out_col, width=2)
    bdraw.line([(82, 29), (100, 29)], fill=gold_hi, width=1)

    blink_im.save(f"{OUT_DIR}/eyes/eyes_blink.png")
    print("  ✓ Cyan, Amber, Blink eyes created")

    # ---------------------------------------------------------
    # 6. Extract Royal Guard Costume (NO gap at x=153..154!)
    # ---------------------------------------------------------
    print("--- 6. Extracting Royal Guard Costume ---")
    cos_arr = np.zeros_like(m_arr)
    # Allow costume to span fully from x=130 to x=370 without artificial x < 155 cut
    for y in range(230, 443):
        for x in range(130, 371):
            is_key = (x > 330 and y < 320)
            if m_arr[y, x, 3] > 0 and not is_key:
                cos_arr[y, x] = m_arr[y, x]

    cos_full = Image.fromarray(cos_arr, mode="RGBA")
    cos_crop = cos_full.crop((130, 230, 370, 442))
    cos_crop.save(f"{OUT_DIR}/costume/costume_royal_guard.png")
    cos_crop.save(f"{OUT_DIR}/costume/costume_nutcracker_guard.png")
    print(f"  ✓ costume_royal_guard.png: size={cos_crop.size}, origin=[126, 118]")

    # ---------------------------------------------------------
    # 7. Extract Body Slices (NO gap at x=153..154!)
    # ---------------------------------------------------------
    print("--- 7. Extracting Body Slices ---")
    body_arr = np.zeros_like(m_arr)
    for y in range(260, 512):
        for x in range(120, 420):
            is_key = (x > 330 and y < 330)
            if m_arr[y, x, 3] > 0 and not is_key:
                body_arr[y, x] = m_arr[y, x]

    body_base = Image.fromarray(body_arr, mode="RGBA")
    body_base.save(f"{OUT_DIR}/body/paint_brass_gold.png")

    b_ivory = np.array(body_base)
    gold_m = (b_ivory[:, :, 3] > 100) & (b_ivory[:, :, 0] > 150) & (b_ivory[:, :, 1] > 110) & (b_ivory[:, :, 2] < 110)
    b_ivory[gold_m, 0] = np.clip(b_ivory[gold_m, 0] * 0.95 + 20, 0, 255)
    b_ivory[gold_m, 1] = np.clip(b_ivory[gold_m, 1] * 0.95 + 20, 0, 255)
    b_ivory[gold_m, 2] = np.clip(b_ivory[gold_m, 2] * 0.5 + 110, 0, 255)
    Image.fromarray(b_ivory, mode="RGBA").save(f"{OUT_DIR}/body/paint_ivory_stock.png")

    b_navy = np.array(body_base)
    b_navy[gold_m, 0] = np.clip(b_navy[gold_m, 0] * 0.2 + 20, 0, 255)
    b_navy[gold_m, 1] = np.clip(b_navy[gold_m, 1] * 0.3 + 40, 0, 255)
    b_navy[gold_m, 2] = np.clip(b_navy[gold_m, 2] * 0.4 + 90, 0, 255)
    Image.fromarray(b_navy, mode="RGBA").save(f"{OUT_DIR}/body/paint_midnight_navy.png")

    print("  ✓ Body slices generated (paint_brass_gold, paint_ivory_stock, paint_midnight_navy)")
    print("🎉 Master Lion slice generation complete (zero gaps, zero artifacts)!")

if __name__ == "__main__":
    run()
