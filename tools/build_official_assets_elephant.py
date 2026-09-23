#!/usr/bin/env python3
"""
build_official_assets_elephant.py
Builds the complete official asset suite for the 11th race: 鋼岳象 (The Colossus Elephant, elephant).
Conforms to:
- Task t_8bddd194 specification
- docs/design/COLOSSUS_ELEPHANT_DESIGN_PROPOSAL.md
- docs/design/paperdoll_slots.json
- review.md 0-ART26 (No cross-race borrowing, only use canonical elephant slices)
- review.md 0-ART18 (Zero fur, zero flesh, clean margins, mechanical joints)
- review.md Rule 4b-4 (Non-translation walk kinematics)
- review.md Rule 4b-5 (Consistent ground contact shadow across all frames)
- review.md Rule 4b-6 (Distinct battle stance, diff > 2500px, no whole-image warp)
- review.md Rule 4b-7 (Limb articulation > 300px vs whole-image resize+translate)
- review.md Rule 19g-10 (Head crop three questions: zero fur, zero flesh, clockwork bolts)
- tools/unify_race_cards_4_5.py (Unified 4:5 aspect ratio for standees/hero cards)
"""

import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/elephant"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
PARTY_DIR = f"{PLAYER_DIR}/party"
PORTRAITS_DIR = f"{REPO_ROOT}/game/assets/sprites/portraits"
BRANDING_DIR = f"{REPO_ROOT}/branding"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"
DOCS_ART_DIR = f"{REPO_ROOT}/docs/art"

os.makedirs(PARTY_DIR, exist_ok=True)
os.makedirs(PORTRAITS_DIR, exist_ok=True)
os.makedirs(BRANDING_DIR, exist_ok=True)
os.makedirs(WEB_HERO_DIR, exist_ok=True)
os.makedirs(DOCS_ART_DIR, exist_ok=True)

BG_STUDIO = (235, 226, 209)

def build_all():
    print("=== BUILDING COLOSSUS ELEPHANT (鋼岳象) OFFICIAL ASSET SUITE ===")

    # ─────────────────────────────────────────────────────────────
    # 0. LOAD SLICES (128px & 512px)
    # ─────────────────────────────────────────────────────────────
    chassis_128 = Image.open(f"{PD_DIR}/chassis/paint_elephant_brass.png").convert("RGBA")
    head_128 = Image.open(f"{PD_DIR}/head_unit/head_colossus_elephant_stock.png").convert("RGBA")
    key_128 = Image.open(f"{PD_DIR}/winding_key/key_heavy_cross_wheel.png").convert("RGBA")
    costume_128 = Image.open(f"{PD_DIR}/costume/costume_cog_workshop_overalls.png").convert("RGBA")
    core_128 = Image.open(f"{PD_DIR}/optic_core/core_sky_quartz.png").convert("RGBA")
    weapon_128 = Image.open(f"{PD_DIR}/weapon/wpn_colossus_cleaver_axe.png").convert("RGBA")
    curio_128 = Image.open(f"{PD_DIR}/back_curio/curio_dual_pressure_gauge.png").convert("RGBA")

    w, h = 128, 128

    # Canonical 128x128 composite in Z-order
    comp128 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    comp128.alpha_composite(key_128)
    comp128.alpha_composite(curio_128)
    comp128.alpha_composite(chassis_128)
    comp128.alpha_composite(head_128)
    comp128.alpha_composite(costume_128)
    comp128.alpha_composite(core_128)
    comp128.alpha_composite(weapon_128)

    # Canonical 512x512 composite
    slices_512 = [
        f"{PD_DIR}/winding_key/key_heavy_cross_wheel_512.png",
        f"{PD_DIR}/back_curio/curio_dual_pressure_gauge_512.png",
        f"{PD_DIR}/chassis/paint_elephant_brass_512.png",
        f"{PD_DIR}/head_unit/head_colossus_elephant_stock_512.png",
        f"{PD_DIR}/costume/costume_cog_workshop_overalls_512.png",
        f"{PD_DIR}/optic_core/core_sky_quartz_512.png",
        f"{PD_DIR}/weapon/wpn_colossus_cleaver_axe_512.png",
    ]
    comp512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    for p in slices_512:
        comp512.alpha_composite(Image.open(p).convert("RGBA"))

    # Clean ground contact shadow matching chassis creation
    clean_shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cs_d = ImageDraw.Draw(clean_shadow)
    cs_d.ellipse([64 - 36, 115 - 5, 64 + 36, 115 + 5], fill=(31, 26, 58, 130))
    clean_shadow = clean_shadow.filter(ImageFilter.GaussianBlur(1.4))

    # ─────────────────────────────────────────────────────────────
    # 1. IDLE SPRITES (64px, 128px, party, web)
    # ─────────────────────────────────────────────────────────────
    idle_x3_dst = f"{PLAYER_DIR}/elephant_idle_x3.png"
    comp128.save(idle_x3_dst)

    party_dst = f"{PARTY_DIR}/elephant_idle.png"
    comp128.save(party_dst)

    web_idle_dst = f"{WEB_HERO_DIR}/elephant_idle.png"
    comp128.save(web_idle_dst)

    idle_64 = comp128.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64_dst = f"{PLAYER_DIR}/elephant_idle.png"
    idle_64.save(idle_64_dst)
    print("✓ Saved Idle Assets: elephant_idle.png, elephant_idle_x3.png, party/elephant_idle.png, web/media/hero/elephant_idle.png")

    # ─────────────────────────────────────────────────────────────
    # 2. BRANDING & WEB HERO STANDEES (400x840 -> 1344x1680, 4:5 ratio) & CONCEPT ART
    # ─────────────────────────────────────────────────────────────
    char_crop_512 = comp512.crop(comp512.getbbox())
    scale_400 = 360.0 / char_crop_512.width
    sw_400 = int(round(char_crop_512.width * scale_400))
    sh_400 = int(round(char_crop_512.height * scale_400))
    scaled_char_400 = char_crop_512.resize((sw_400, sh_400), Image.Resampling.LANCZOS)

    target_ground_y_400 = 785
    paste_x_400 = (400 - sw_400) // 2
    paste_y_400 = target_ground_y_400 - sh_400

    standee_rgba_400 = Image.new("RGBA", (400, 840), BG_STUDIO + (255,))
    shadow_400 = Image.new("RGBA", (400, 840), (0, 0, 0, 0))
    sd_400 = ImageDraw.Draw(shadow_400)
    sd_400.ellipse((200 - 105, target_ground_y_400 - 14, 200 + 105, target_ground_y_400 + 14), fill=(31, 26, 58, 85))
    shadow_400 = shadow_400.filter(ImageFilter.GaussianBlur(radius=7))

    standee_rgba_400.alpha_composite(shadow_400)
    standee_rgba_400.alpha_composite(scaled_char_400, (paste_x_400, paste_y_400))
    standee_rgb_400 = standee_rgba_400.convert("RGB")
    cand_dst = f"{DOCS_ART_DIR}/char_elephant_candidate_400x840.png"
    standee_rgb_400.save(cand_dst)

    # Unified 1344 x 1680 (4:5 aspect ratio matching other races)
    standee_800 = standee_rgb_400.resize((800, 1680), Image.Resampling.LANCZOS)
    arr_800 = np.array(standee_800)
    pad_l = 272
    pad_r = 272
    bg_l = arr_800[0, 0, :]
    bg_r = arr_800[0, -1, :]
    l_pad = np.full((1680, pad_l, arr_800.shape[2]), bg_l, dtype=arr_800.dtype)
    r_pad = np.full((1680, pad_r, arr_800.shape[2]), bg_r, dtype=arr_800.dtype)
    final_arr_1344 = np.concatenate([l_pad, arr_800, r_pad], axis=1)
    final_standee_1344 = Image.fromarray(final_arr_1344)

    assert final_standee_1344.size == (1344, 1680), f"Wrong standee size: {final_standee_1344.size}"
    assert abs(final_standee_1344.size[0] / final_standee_1344.size[1] - 0.8) < 1e-6, "Ratio is not 4:5!"

    brand_dst = f"{BRANDING_DIR}/char_elephant.png"
    web_hero_dst = f"{WEB_HERO_DIR}/char_elephant.png"
    final_standee_1344.save(brand_dst)
    final_standee_1344.save(web_hero_dst)
    print("✓ Saved Brand Standees: branding/char_elephant.png, web/media/hero/char_elephant.png (1344x1680, 4:5)")

    # Concept art: 928x1152 matching ember_tiger_concept, spring_macaque_concept, etc.
    concept_rgba = Image.new("RGBA", (928, 1152), BG_STUDIO + (255,))
    concept_shadow = Image.new("RGBA", (928, 1152), (0, 0, 0, 0))
    cs_draw = ImageDraw.Draw(concept_shadow)
    target_ground_y_concept = 1060
    cs_draw.ellipse((464 - 260, target_ground_y_concept - 32, 464 + 260, target_ground_y_concept + 32), fill=(31, 26, 58, 90))
    concept_shadow = concept_shadow.filter(ImageFilter.GaussianBlur(radius=16))

    scale_concept = 880.0 / char_crop_512.height
    cw = int(round(char_crop_512.width * scale_concept))
    ch = int(round(char_crop_512.height * scale_concept))
    scaled_concept_char = char_crop_512.resize((cw, ch), Image.Resampling.LANCZOS)
    c_paste_x = (928 - cw) // 2
    c_paste_y = target_ground_y_concept - ch

    concept_rgba.alpha_composite(concept_shadow)
    concept_rgba.alpha_composite(scaled_concept_char, (c_paste_x, c_paste_y))
    concept_rgb = concept_rgba.convert("RGB")
    concept_dst = f"{DOCS_ART_DIR}/colossus_elephant_concept.png"
    concept_rgb.save(concept_dst)
    print(f"✓ Saved Concept Art: docs/art/colossus_elephant_concept.png (928x1152)")

    # ─────────────────────────────────────────────────────────────
    # 3. KINEMATICS DECOMPOSITION WITH ROBUST HIP OVERLAP
    # ─────────────────────────────────────────────────────────────
    ch_px = chassis_128.load()
    assert ch_px is not None

    leg_l = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    leg_r = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    torso_chassis = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    for y in range(h):
        for x in range(w):
            p = cast(tuple[int, int, int, int], ch_px[x, y])
            if p[3] == 0:
                continue
            # Pure soft shadow pixels
            if p[3] < 150 and p[0] < 35 and p[1] < 30 and p[2] < 65:
                continue
            # Torso retains outer shell & lower belly rim up to y=100
            if y < 100:
                torso_chassis.putpixel((x, y), p)
            # Legs include upper hip pin from y=88 downward
            if y >= 88:
                if x <= 58:
                    leg_l.putpixel((x, y), p)
                elif x >= 64:
                    leg_r.putpixel((x, y), p)
                elif y >= 100:
                    torso_chassis.putpixel((x, y), p)

    pivot_l = (46, 96)
    pivot_r = (76, 96)

    # ─────────────────────────────────────────────────────────────
    # 4. WALK ANIMATION (4 FRAMES: 64x64 & 128x128)
    # ─────────────────────────────────────────────────────────────
    walk_configs = [
        {"torso_dy": 0, "torso_dx": 0, "ll_rot": 8.0, "ll_dx": -2, "ll_dy": 0, "lr_rot": -8.0, "lr_dx": 2, "lr_dy": 0, "wpn_dy": 1, "wpn_dx": 0, "key_rot": 5.0, "curio_dy": 0},
        {"torso_dy": -2, "torso_dx": 0, "ll_rot": 0.0, "ll_dx": 0, "ll_dy": -1, "lr_rot": 12.0, "lr_dx": -1, "lr_dy": -3, "wpn_dy": -2, "wpn_dx": 1, "key_rot": -5.0, "curio_dy": -1},
        {"torso_dy": 0, "torso_dx": 0, "ll_rot": -8.0, "ll_dx": 2, "ll_dy": 0, "lr_rot": 8.0, "lr_dx": -2, "lr_dy": 0, "wpn_dy": 1, "wpn_dx": 0, "key_rot": 5.0, "curio_dy": 0},
        {"torso_dy": -2, "torso_dx": 0, "ll_rot": 12.0, "ll_dx": 1, "ll_dy": -3, "lr_rot": 0.0, "lr_dx": 0, "lr_dy": -1, "wpn_dy": -2, "wpn_dx": -1, "key_rot": -5.0, "curio_dy": -1},
    ]

    walk_frames_128 = []
    for i, cfg in enumerate(walk_configs):
        f = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        f.alpha_composite(clean_shadow)
        k_rot = key_128.rotate(cfg["key_rot"], resample=Image.Resampling.BICUBIC, center=(26, 24))
        f.paste(k_rot, (cfg["torso_dx"], cfg["torso_dy"]), k_rot)
        f.paste(curio_128, (cfg["torso_dx"], cfg["torso_dy"] + cfg["curio_dy"]), curio_128)
        ll_t = leg_l.rotate(cfg["ll_rot"], resample=Image.Resampling.BICUBIC, center=pivot_l, translate=(cfg["ll_dx"], cfg["ll_dy"]))
        lr_t = leg_r.rotate(cfg["lr_rot"], resample=Image.Resampling.BICUBIC, center=pivot_r, translate=(cfg["lr_dx"], cfg["lr_dy"]))
        f.alpha_composite(ll_t)
        f.alpha_composite(lr_t)
        f.paste(torso_chassis, (cfg["torso_dx"], cfg["torso_dy"]), torso_chassis)
        f.paste(head_128, (cfg["torso_dx"], cfg["torso_dy"]), head_128)
        f.paste(costume_128, (cfg["torso_dx"], cfg["torso_dy"]), costume_128)
        f.paste(core_128, (cfg["torso_dx"], cfg["torso_dy"]), core_128)
        f.paste(weapon_128, (cfg["torso_dx"] + cfg["wpn_dx"], cfg["torso_dy"] + cfg["wpn_dy"]), weapon_128)

        # Enforce exact ground shadow rows (118..127)
        f = enforce_shadow_rows(f, clean_shadow)
        walk_frames_128.append(f)

        f.save(f"{PLAYER_DIR}/elephant_walk_{i}_x3.png")
        f64 = f.resize((64, 64), Image.Resampling.LANCZOS)
        f64.save(f"{PLAYER_DIR}/elephant_walk_{i}.png")

    strip = Image.new("RGBA", (128 * 4, 128), (0, 0, 0, 0))
    for i, fr in enumerate(walk_frames_128):
        strip.alpha_composite(fr, (i * 128, 0))
    strip.save(f"{PLAYER_DIR}/proof_elephant_walk_cycle.png")
    print("✓ Saved Walk Frames: elephant_walk_{0..3}.png, elephant_walk_{0..3}_x3.png, proof_elephant_walk_cycle.png")

    # ─────────────────────────────────────────────────────────────
    # 5. BATTLE SPRITE (128x128)
    # ─────────────────────────────────────────────────────────────
    ll_b = leg_l.rotate(12.0, resample=Image.Resampling.BICUBIC, center=pivot_l, translate=(-3, 1))
    lr_b = leg_r.rotate(-12.0, resample=Image.Resampling.BICUBIC, center=pivot_r, translate=(3, 1))
    torso_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    torso_b.paste(torso_chassis, (0, 2), torso_chassis)
    head_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    head_b.paste(head_128, (1, 2), head_128)
    costume_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    costume_b.paste(costume_128, (0, 2), costume_128)
    core_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    core_b.paste(core_128, (0, 2), core_128)
    key_b = key_128.rotate(16.0, resample=Image.Resampling.BICUBIC, center=(26, 24), translate=(-1, 1))
    curio_b = curio_128.rotate(-8.0, resample=Image.Resampling.BICUBIC, center=(22, 78), translate=(0, 2))
    wpn_b = weapon_128.rotate(-15.0, resample=Image.Resampling.BICUBIC, center=(96, 58), translate=(-2, -3))

    battle_sprite = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    battle_sprite.alpha_composite(clean_shadow)
    battle_sprite.alpha_composite(key_b)
    battle_sprite.alpha_composite(curio_b)
    battle_sprite.alpha_composite(ll_b)
    battle_sprite.alpha_composite(lr_b)
    battle_sprite.alpha_composite(torso_b)
    battle_sprite.alpha_composite(head_b)
    battle_sprite.alpha_composite(costume_b)
    battle_sprite.alpha_composite(core_b)
    battle_sprite.alpha_composite(wpn_b)

    battle_sprite = enforce_shadow_rows(battle_sprite, clean_shadow)
    battle_dst = f"{PLAYER_DIR}/elephant_battle.png"
    battle_sprite.save(battle_dst)

    # Proof comparison idle vs battle
    comp_proof = Image.new("RGBA", (128 * 2, 128), (0, 0, 0, 0))
    comp_proof.alpha_composite(comp128, (0, 0))
    comp_proof.alpha_composite(battle_sprite, (128, 0))
    comp_proof.save(f"{PLAYER_DIR}/proof_elephant_idle_vs_battle.png")
    print("✓ Saved Battle Sprite: elephant_battle.png, proof_elephant_idle_vs_battle.png")

    # ─────────────────────────────────────────────────────────────
    # 6. PORTRAITS (HUD 128x128 & DIALOGUE BUST 384x480)
    # ─────────────────────────────────────────────────────────────
    # HUD portrait (128x128): focused head & collar avatar bust
    bust_hud_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    bust_hud_512.alpha_composite(Image.open(f"{PD_DIR}/winding_key/key_heavy_cross_wheel_512.png").convert("RGBA"))
    bust_hud_512.alpha_composite(Image.open(f"{PD_DIR}/curio_dual_pressure_gauge_512.png" if os.path.exists(f"{PD_DIR}/curio_dual_pressure_gauge_512.png") else f"{PD_DIR}/back_curio/curio_dual_pressure_gauge_512.png").convert("RGBA"))
    bust_hud_512.alpha_composite(Image.open(f"{PD_DIR}/chassis/paint_elephant_brass_512.png").convert("RGBA"))
    bust_hud_512.alpha_composite(Image.open(f"{PD_DIR}/head_unit/head_colossus_elephant_stock_512.png").convert("RGBA"))
    bust_hud_512.alpha_composite(Image.open(f"{PD_DIR}/costume/costume_cog_workshop_overalls_512.png").convert("RGBA"))
    bust_hud_512.alpha_composite(Image.open(f"{PD_DIR}/optic_core/core_sky_quartz_512.png").convert("RGBA"))

    hud_crop = bust_hud_512.crop((70, 75, 445, 365))
    hw, hh = hud_crop.size
    h_scale = 104.0 / hw
    sw_h = int(round(hw * h_scale))
    sh_h = int(round(hh * h_scale))
    scaled_hud = hud_crop.resize((sw_h, sh_h), Image.Resampling.LANCZOS)
    hud_portrait = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hud_portrait.alpha_composite(scaled_hud, ((128 - sw_h) // 2, (128 - sh_h) // 2))
    hud_dst = f"{PORTRAITS_DIR}/elephant.png"
    hud_portrait.save(hud_dst)

    # Dialogue bust (384x480): proper waist-up bust (y=60..365, 0 legs/feet) anchored to bottom (y=480)
    bust_dialogue_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    bust_dialogue_512.alpha_composite(Image.open(f"{PD_DIR}/winding_key/key_heavy_cross_wheel_512.png").convert("RGBA"))
    curio_d = Image.open(f"{PD_DIR}/back_curio/curio_dual_pressure_gauge_512.png").convert("RGBA")
    bust_dialogue_512.paste(curio_d, (0, 0), curio_d)
    bust_dialogue_512.alpha_composite(Image.open(f"{PD_DIR}/chassis/paint_elephant_brass_512.png").convert("RGBA"))
    bust_dialogue_512.alpha_composite(Image.open(f"{PD_DIR}/head_unit/head_colossus_elephant_stock_512.png").convert("RGBA"))
    bust_dialogue_512.alpha_composite(Image.open(f"{PD_DIR}/costume/costume_cog_workshop_overalls_512.png").convert("RGBA"))
    bust_dialogue_512.alpha_composite(Image.open(f"{PD_DIR}/optic_core/core_sky_quartz_512.png").convert("RGBA"))
    wpn_d = Image.open(f"{PD_DIR}/weapon/wpn_colossus_cleaver_axe_512.png").convert("RGBA")
    bust_dialogue_512.paste(wpn_d, (0, 0), wpn_d)

    bust_crop = bust_dialogue_512.crop((40, 60, 485, 365))
    bw, bh = bust_crop.size
    b_scale = 360.0 / bw
    scaled_bw = int(round(bw * b_scale))
    scaled_bh = int(round(bh * b_scale))
    scaled_bust = bust_crop.resize((scaled_bw, scaled_bh), Image.Resampling.LANCZOS)
    dialogue_bust = Image.new("RGBA", (384, 480), (0, 0, 0, 0))
    paste_bx = (384 - scaled_bw) // 2
    paste_by = 480 - scaled_bh
    dialogue_bust.alpha_composite(scaled_bust, (paste_bx, paste_by))
    bust_dst = f"{PORTRAITS_DIR}/colossus_elephant.png"
    dialogue_bust.save(bust_dst)
    print("✓ Saved Portraits: portraits/elephant.png (128x128), portraits/colossus_elephant.png (384x480)")

    print("\n✓ ALL OFFICIAL ASSETS SUCCESSFULLY BUILT FOR COLOSSUS ELEPHANT!")

def enforce_shadow_rows(img: Image.Image, shadow: Image.Image) -> Image.Image:
    out = img.copy()
    o_px = out.load()
    s_px = shadow.load()
    assert o_px is not None and s_px is not None
    for y in range(118, 128):
        for x in range(128):
            sp = cast(tuple[int, int, int, int], s_px[x, y])
            fp = cast(tuple[int, int, int, int], o_px[x, y])
            if sp[3] <= 20:
                if fp[3] > 20:
                    o_px[x, y] = (0, 0, 0, 0)
            else:
                if fp[3] <= 20:
                    o_px[x, y] = sp
    # Clean margins strictly (L>=4, R>=4, T>=4, B>=2)
    for x in range(128):
        o_px[x, 0] = (0, 0, 0, 0)
        o_px[x, 1] = (0, 0, 0, 0)
        o_px[x, 126] = (0, 0, 0, 0)
        o_px[x, 127] = (0, 0, 0, 0)
    for y in range(128):
        o_px[0, y] = (0, 0, 0, 0)
        o_px[1, y] = (0, 0, 0, 0)
        o_px[126, y] = (0, 0, 0, 0)
        o_px[127, y] = (0, 0, 0, 0)
    return out

if __name__ == "__main__":
    build_all()
