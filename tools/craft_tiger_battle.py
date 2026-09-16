#!/usr/bin/env python3
import os
from typing import cast
from PIL import Image, ImageChops
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
TIGER_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/tiger"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"

def craft_battle_sprite():
    chassis = Image.open(f"{TIGER_PD}/chassis/paint_ember_orange.png").convert("RGBA")
    head = Image.open(f"{TIGER_PD}/head_unit/head_ember_tiger_stock.png").convert("RGBA")
    key = Image.open(f"{TIGER_PD}/winding_key/key_turbine_flame.png").convert("RGBA")
    costume = Image.open(f"{TIGER_PD}/costume/costume_ember_tunic.png").convert("RGBA")
    core = Image.open(f"{TIGER_PD}/optic_core/core_molten_amber.png").convert("RGBA")
    tail = Image.open(f"{TIGER_PD}/back_curio/curio_exhaust_tiger_tail.png").convert("RGBA")
    dual_wpn = Image.open(f"{TIGER_PD}/weapon/wpn_twin_ember_sabers.png").convert("RGBA")
    
    w, h = 128, 128
    
    # 1. Separate dual weapon into main-hand and off-hand components
    # Main hand saber: x >= 65
    # Off hand saber: x < 65
    w_arr = np.array(dual_wpn)
    main_saber = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    off_saber = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y in range(h):
        for x in range(w):
            if w_arr[y, x, 3] > 0:
                if x >= 65:
                    main_saber.putpixel((x, y), tuple(w_arr[y, x]))
                else:
                    off_saber.putpixel((x, y), tuple(w_arr[y, x]))
                    
    # 2. Base ground shadow at y >= 118:
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ch_px = chassis.load()
    sh_px = shadow.load()
    assert ch_px is not None and sh_px is not None
    
    for y in range(118, 128):
        for x in range(w):
            p = cast(tuple[int, int, int, int], ch_px[x, y])
            if p[3] > 15:
                sh_px[x, y] = p
                if 40 <= x <= 50 and x - 8 >= 0:
                    sh_px[x - 8, y] = (p[0], p[1], p[2], int(p[3] * 0.8))
                if 80 <= x <= 90 and x + 8 < 128:
                    sh_px[x + 8, y] = (p[0], p[1], p[2], int(p[3] * 0.8))
    sh_px[64, 124] = (0, 0, 0, 0)

    # 3. Decompose chassis
    leg_l = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    leg_r = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pelvis = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    torso_chassis = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    
    for y in range(h):
        for x in range(w):
            p = cast(tuple[int, int, int, int], ch_px[x, y])
            if p[3] == 0:
                continue
            if y >= 118:
                if p[0] > 120 or p[1] > 60:
                    if x <= 65:
                        leg_l.putpixel((x, y), p)
                    else:
                        leg_r.putpixel((x, y), p)
                continue
            if y < 88:
                torso_chassis.putpixel((x, y), p)
            elif 88 <= y < 98:
                if 55 <= x <= 77:
                    pelvis.putpixel((x, y), p)
                if x <= 65:
                    leg_l.putpixel((x, y), p)
                else:
                    leg_r.putpixel((x, y), p)
            else:
                if x <= 65:
                    leg_l.putpixel((x, y), p)
                else:
                    leg_r.putpixel((x, y), p)

    # 4. Aggressive combat crouch kinematics:
    pivot_l = (55, 94)
    pivot_r = (76, 94)
    
    ll_crouch = leg_l.rotate(22.0, resample=Image.Resampling.BICUBIC, center=pivot_l, translate=(-8, 2))
    lr_crouch = leg_r.rotate(-22.0, resample=Image.Resampling.BICUBIC, center=pivot_r, translate=(8, 2))
    
    p_crouch = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    p_crouch.paste(pelvis, (-3, 6), pelvis)
    
    tc_crouch = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    tc_crouch.paste(torso_chassis, (-3, 6), torso_chassis)
    
    c_crouch = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    c_crouch.paste(costume, (-3, 6), costume)
    
    core_crouch = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    core_crouch.paste(core, (-3, 6), core)
    
    h_crouch = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    h_crouch.paste(head, (-4, 6), head)
    
    k_crouch = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    k_crouch.paste(key, (-3, 6), key)
    
    tail_crouch = tail.rotate(14.0, resample=Image.Resampling.BICUBIC, center=(52, 98), translate=(-1, 4))
    
    # 5. Weapons in combat stance:
    # Main hand (right): swing forward to thrusting angle
    main_crouch = main_saber.rotate(-48.0, resample=Image.Resampling.BICUBIC, center=(88, 76), translate=(-14, 8))
    # Off hand (left): reverse grip saber held in left hand, blade pointing backward/down along the side
    off_crouch = off_saber.rotate(-36.0, resample=Image.Resampling.BICUBIC, center=(38, 77), translate=(-3, 6))
    
    # 6. Composite final battle sprite in canonical Z-order:
    battle_sprite = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    battle_sprite.alpha_composite(shadow)     # Base ground shadow
    battle_sprite.alpha_composite(k_crouch)   # Z: 5 Winding key
    battle_sprite.alpha_composite(tail_crouch)# Z: 8 Tail
    battle_sprite.alpha_composite(lr_crouch)  # Rear leg
    battle_sprite.alpha_composite(p_crouch)   # Pelvis
    battle_sprite.alpha_composite(ll_crouch)  # Front leg
    battle_sprite.alpha_composite(tc_crouch)  # Z: 10 Chassis
    battle_sprite.alpha_composite(h_crouch)   # Z: 20 Head
    battle_sprite.alpha_composite(c_crouch)   # Z: 25 Costume
    battle_sprite.alpha_composite(core_crouch)# Z: 30 Core
    battle_sprite.alpha_composite(main_crouch)# Z: 40 Main Weapon
    battle_sprite.alpha_composite(off_crouch) # Z: 40 Off Weapon
    
    # Enforce Rule 4b-5 shadow constraints:
    b_px = battle_sprite.load()
    assert b_px is not None
    for sy in range(118, 128):
        for sx in range(128):
            sp = cast(tuple[int, int, int, int], sh_px[sx, sy])
            fp = cast(tuple[int, int, int, int], b_px[sx, sy])
            if sp[3] <= 20 and fp[3] > 20:
                b_px[sx, sy] = (0, 0, 0, 0)
            elif sp[3] > 20 and fp[3] <= 20:
                b_px[sx, sy] = sp

    # 7. Verification vs idle
    idle_img = Image.open(f"{PLAYER_DIR}/party/tiger_idle.png").convert("RGBA")
    diff_idle = ImageChops.difference(idle_img, battle_sprite)
    diff_bbox = diff_idle.getbbox()
    d_px = diff_idle.load()
    assert d_px is not None
    changed_px = sum(1 for y in range(128) for x in range(128) if cast(tuple[int, int, int, int], d_px[x, y])[3] > 10)
    print(f"Battle vs Idle diff bbox: {diff_bbox}, changed pixels: {changed_px} ({changed_px/16384*100:.1f}%)")
    
    b_bbox = battle_sprite.getbbox()
    assert b_bbox is not None
    print(f"Battle sprite full bbox: {b_bbox} (Left margin = {b_bbox[0]}px, Top margin = {b_bbox[1]}px)")
    assert b_bbox[0] >= 4, f"Blade or character too close to left border: {b_bbox[0]}px"
    
    dst = f"{PLAYER_DIR}/tiger_battle.png"
    battle_sprite.save(dst)
    print(f"✓ Saved {dst}")

if __name__ == "__main__":
    craft_battle_sprite()
