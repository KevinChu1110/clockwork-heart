#!/usr/bin/env python3
import os
from typing import cast
from PIL import Image, ImageChops
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
TIGER_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/tiger"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

def build_walk_assets():
    chassis = Image.open(f"{TIGER_PD}/chassis/paint_ember_orange.png").convert("RGBA")
    head = Image.open(f"{TIGER_PD}/head_unit/head_ember_tiger_stock.png").convert("RGBA")
    key = Image.open(f"{TIGER_PD}/winding_key/key_turbine_flame.png").convert("RGBA")
    costume = Image.open(f"{TIGER_PD}/costume/costume_ember_tunic.png").convert("RGBA")
    core = Image.open(f"{TIGER_PD}/optic_core/core_molten_amber.png").convert("RGBA")
    tail = Image.open(f"{TIGER_PD}/back_curio/curio_exhaust_tiger_tail.png").convert("RGBA")
    dual_wpn = Image.open(f"{TIGER_PD}/weapon/wpn_twin_ember_sabers.png").convert("RGBA")
    
    w, h = 128, 128
    
    # 1. Separate dual weapon into main-hand and off-hand components
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
                    
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ch_px = chassis.load()
    sh_px = shadow.load()
    assert ch_px is not None and sh_px is not None
    
    for y in range(118, 128):
        for x in range(w):
            p = cast(tuple[int, int, int, int], ch_px[x, y])
            if p[3] > 15:
                sh_px[x, y] = p

    # Rule 4b-5: remove the single 1-pixel spur at (64, 124) so shadow bottom is a smooth clean ellipse
    sh_px[64, 124] = (0, 0, 0, 0)
                
    sh_counts = [sum(1 for x in range(128) if cast(tuple[int, int, int, int], sh_px[x, y])[3] > 20) for y in range(118, 128)]
    print("Clean base shadow row counts (y=118..127):", sh_counts)
    
    # Decompose chassis
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

    pivot_l = (55, 94)
    pivot_r = (76, 94)
    tail_pivot = (52, 98)
    
    gait_configs = [
        # Frame 0: Contact 1 (Left forward stride, Left arm swings rearward)
        {
            "torso_dy": 0,
            "leg_l_rot": 8.0, "leg_l_dx": -2, "leg_l_dy": 0,
            "leg_r_rot": -8.0, "leg_r_dx": 2, "leg_r_dy": 0,
            "tail_rot": 2.0, "tail_dx": 0, "tail_dy": 0,
            "main_rot": -5.0, "main_dy": 0,
            "off_rot": -24.0, "off_dx": 4, "off_dy": 0,
        },
        # Frame 1: Passing 1 (Up-bob -3px, Left supporting, Right swinging forward lifted 6px)
        {
            "torso_dy": -3,
            "leg_l_rot": 0.0, "leg_l_dx": 0, "leg_l_dy": 0,
            "leg_r_rot": 14.0, "leg_r_dx": -3, "leg_r_dy": -6,
            "tail_rot": -2.0, "tail_dx": 0, "tail_dy": -2,
            "main_rot": 4.0, "main_dy": -3,
            "off_rot": 0.0, "off_dx": 0, "off_dy": -3,
        },
        # Frame 2: Contact 2 (Right forward stride, Left arm swings forward)
        {
            "torso_dy": 0,
            "leg_l_rot": -8.0, "leg_l_dx": 2, "leg_l_dy": 0,
            "leg_r_rot": 8.0, "leg_r_dx": -2, "leg_r_dy": 0,
            "tail_rot": 2.0, "tail_dx": 0, "tail_dy": 0,
            "main_rot": -5.0, "main_dy": 0,
            "off_rot": 22.0, "off_dx": -5, "off_dy": 0,
        },
        # Frame 3: Passing 2 (Up-bob -3px, Right supporting, Left swinging forward lifted 6px)
        {
            "torso_dy": -3,
            "leg_l_rot": 14.0, "leg_l_dx": -3, "leg_l_dy": -6,
            "leg_r_rot": 0.0, "leg_r_dx": 0, "leg_r_dy": 0,
            "tail_rot": -2.0, "tail_dx": 0, "tail_dy": -2,
            "main_rot": 4.0, "main_dy": -3,
            "off_rot": 0.0, "off_dx": 0, "off_dy": -3,
        },
    ]

    frames_128 = []
    
    for idx, cfg in enumerate(gait_configs):
        tdy = cfg["torso_dy"]
        frame = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        
        # 1. Base shadow layer
        frame.alpha_composite(shadow)
        
        # 2. Tail layer
        t_shift = tail.rotate(cfg["tail_rot"], resample=Image.Resampling.BICUBIC, center=tail_pivot, translate=(cfg["tail_dx"], cfg["tail_dy"]))
        frame.alpha_composite(t_shift)
        
        # 3. Legs
        lr = leg_r.rotate(cfg["leg_r_rot"], resample=Image.Resampling.BICUBIC, center=pivot_r, translate=(cfg["leg_r_dx"], cfg["leg_r_dy"]))
        ll = leg_l.rotate(cfg["leg_l_rot"], resample=Image.Resampling.BICUBIC, center=pivot_l, translate=(cfg["leg_l_dx"], cfg["leg_l_dy"]))
        
        p_shift = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        p_shift.paste(pelvis, (0, tdy), pelvis)
        
        if idx in (0, 1):
            frame.alpha_composite(lr)
            frame.alpha_composite(p_shift)
            frame.alpha_composite(ll)
        else:
            frame.alpha_composite(ll)
            frame.alpha_composite(p_shift)
            frame.alpha_composite(lr)
            
        # 4. Winding key (Z: 5)
        k_shift = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        k_shift.paste(key, (0, tdy), key)
        frame.alpha_composite(k_shift)
        
        # 5. Torso chassis (Z: 10)
        tc_shift = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        tc_shift.paste(torso_chassis, (0, tdy), torso_chassis)
        frame.alpha_composite(tc_shift)
        
        # 6. Head (Z: 20)
        h_shift = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        h_shift.paste(head, (0, tdy), head)
        frame.alpha_composite(h_shift)
        
        # 7. Costume (Z: 25)
        c_shift = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        c_shift.paste(costume, (0, tdy), costume)
        frame.alpha_composite(c_shift)
        
        # 8. Core (Z: 30)
        core_shift = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        core_shift.paste(core, (0, tdy), core)
        frame.alpha_composite(core_shift)
        
        # 9. Dual Weapons (Z: 40)
        # Main hand saber:
        m_shift = main_saber.rotate(cfg["main_rot"], resample=Image.Resampling.BICUBIC, center=(88, 76), translate=(0, cfg["main_dy"]))
        frame.alpha_composite(m_shift)
        
        # Off hand saber:
        o_shift = off_saber.rotate(cfg["off_rot"], resample=Image.Resampling.BICUBIC, center=(38, 77), translate=(cfg["off_dx"], cfg["off_dy"]))
        frame.alpha_composite(o_shift)
        
        # 10. Rule 4b-5 strict shadow constraint:
        fr_px = frame.load()
        assert fr_px is not None
        for sy in range(118, 128):
            for sx in range(128):
                sp = cast(tuple[int, int, int, int], sh_px[sx, sy])
                fp = cast(tuple[int, int, int, int], fr_px[sx, sy])
                if sp[3] <= 20 and fp[3] > 20:
                    fr_px[sx, sy] = (0, 0, 0, 0)
                elif sp[3] > 20 and fp[3] <= 20:
                    fr_px[sx, sy] = sp
        
        frames_128.append(frame)

    # 4. Save all walk assets:
    for i, fr in enumerate(frames_128):
        p128 = f"{PLAYER_DIR}/tiger_walk_{i}_x3.png"
        fr.save(p128)
        print(f"✓ Saved {p128}")
        
        fr64 = fr.resize((64, 64), Image.Resampling.LANCZOS)
        p64 = f"{PLAYER_DIR}/tiger_walk_{i}.png"
        fr64.save(p64)
        print(f"✓ Saved {p64}")

    # 5. Save standard idle assets:
    comp = Image.open(f"{TIGER_PD}/proof_paperdoll_tiger_composite.png").convert("RGBA")
    party_p = f"{PLAYER_DIR}/party/tiger_idle.png"
    comp.save(party_p)
    print(f"✓ Saved {party_p}")
    
    idle_x3_p = f"{PLAYER_DIR}/tiger_idle_x3.png"
    comp.save(idle_x3_p)
    print(f"✓ Saved {idle_x3_p}")
    
    idle_64 = comp.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64_p = f"{PLAYER_DIR}/tiger_idle.png"
    idle_64.save(idle_64_p)
    print(f"✓ Saved {idle_64_p}")
    
    hero_idle_p = f"{WEB_HERO_DIR}/tiger_idle.png"
    comp.save(hero_idle_p)
    print(f"✓ Saved {hero_idle_p}")

    # 6. Save walk cycle proof (strip)
    walk_strip = Image.new("RGBA", (128 * 4, 128), (0, 0, 0, 0))
    for i, fr in enumerate(frames_128):
        walk_strip.alpha_composite(fr, (i * 128, 0))
    proof_p = f"{PLAYER_DIR}/proof_tiger_walk_cycle.png"
    walk_strip.save(proof_p)
    print(f"✓ Saved {proof_p}")

    # 7. Save idle vs battle comparison proof:
    battle_p = f"{PLAYER_DIR}/tiger_battle.png"
    if os.path.exists(battle_p):
        bat = Image.open(battle_p).convert("RGBA")
        comp_proof = Image.new("RGBA", (256, 128), (0, 0, 0, 0))
        comp_proof.alpha_composite(comp, (0, 0))
        comp_proof.alpha_composite(bat, (128, 0))
        comp_proof.save(f"{PLAYER_DIR}/proof_tiger_idle_vs_battle.png")
        print(f"✓ Saved {PLAYER_DIR}/proof_tiger_idle_vs_battle.png")

if __name__ == "__main__":
    build_walk_assets()
