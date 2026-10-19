#!/usr/bin/env python3
"""
tools/render_clear_z_order_proof.py
Generates proof_maple_lion_z_order_swap.png where Z-order changes are crystal clear:
Left: Weapon in hand (Z=40, in front of body/arm), Winding Key on back (Z=5, behind body).
Right: Weapon slung behind body (Z=4), Winding Key brought to front (Z=15, overlapping body).
"""

import math
import numpy as np
from PIL import Image

WS_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a"
MASTER_P = f"{WS_ROOT}/tools/lion_master_512.png"
PARTS_DIR = f"{WS_ROOT}/game/assets/sprites/player/paperdoll/lion/maple_parts"
PROOF_DIR = f"{WS_ROOT}/game/assets/sprites/player/paperdoll/lion"

def get_layer(slot, item):
    if item in ("none", "", None):
        return None
    p = f"{PARTS_DIR}/{slot}/{item}.png"
    return Image.open(p).convert("RGBA")

def composite_lion(weapon_z=40, key_z=5, weapon_pos=(75, 27), weapon_rot=0.0):
    layers = []

    # Winding Key (pivot 342, 296, origin 20, 113 -> dest 322, 183)
    k_img = get_layer("winding_key", "key_classic_brass")
    if k_img:
        layers.append((key_z, k_img, (322, 183)))

    # Back Curio
    c_img = get_layer("back_curio", "curio_lion_fan_tail")
    if c_img:
        layers.append((8, c_img, (351, 364)))

    # Body
    b_img = get_layer("body", "paint_brass_gold")
    if b_img:
        layers.append((10, b_img, (0, 0)))

    # Head unit
    h_img = get_layer("head_unit", "ear_lion_gilded_mane_brass")
    if h_img:
        layers.append((20, h_img, (131, 51)))

    # Costume
    cos_img = get_layer("costume", "costume_royal_guard")
    if cos_img:
        layers.append((25, cos_img, (130, 230)))

    # Eyes
    e_img = get_layer("eyes", "eyes_amber_gold")
    if e_img:
        layers.append((30, e_img, (168, 143)))

    # Weapon
    w_img = get_layer("weapon", "wpn_knight_lance")
    if w_img:
        if abs(weapon_rot) > 0.001:
            w_rot = w_img.rotate(math.degrees(weapon_rot), resample=Image.Resampling.BICUBIC, expand=True)
            layers.append((weapon_z, w_rot, weapon_pos))
        else:
            layers.append((weapon_z, w_img, weapon_pos))

    layers.sort(key=lambda x: x[0])

    comp = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    for z, img, pos in layers:
        comp.alpha_composite(img, pos)

    return comp

def run():
    print("--- Rendering Proof D: Z-Order Swap ---")
    cream = (255, 252, 247, 255)
    proof_d = Image.new("RGBA", (512 * 2, 512), cream)

    # Left: Weapon in Hand (Z=40, front), Key behind (Z=5, back)
    d_left = composite_lion(weapon_z=40, key_z=5)

    # Right: Weapon behind Back (Z=4, slung across back at x=200, y=40, rot=0.45 rad), Key behind (Z=5)
    d_right = composite_lion(weapon_z=4, key_z=5, weapon_pos=(180, 20), weapon_rot=0.42)

    proof_d.alpha_composite(d_left, (0, 0))
    proof_d.alpha_composite(d_right, (512, 0))
    proof_d.save(f"{PROOF_DIR}/proof_maple_lion_z_order_swap.png")
    print(f"  ✓ Saved {PROOF_DIR}/proof_maple_lion_z_order_swap.png")

if __name__ == "__main__":
    run()
