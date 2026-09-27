#!/usr/bin/env python3
"""
build_official_assets_kangaroo.py
Builds the complete official asset suite for the 24th race: 鐵拳袋鼠 (The Boxer Kangaroo, kangaroo).
Conforms to:
- Task t_d1581027 specification
- docs/design/BOXER_KANGAROO_DESIGN_PROPOSAL.md
- docs/design/paperdoll_slots.json
- review.md 0-ART25 (showcase/*_idle_hd.png RGBA mode and 4-corner alpha=0 check)
- review.md 0-ART26 (No cross-race borrowing, only use canonical kangaroo slices)
- review.md 0-ART18 (Zero fur, zero flesh, clean margins, mechanical joints)
- review.md 0-MKT7 (Single-wield pneumatic piston brass knuckle on right hand)
- review.md Rule 4b-4 (Non-translation walk kinematics)
- review.md Rule 4b-5 (Consistent ground contact shadow across all frames: [68, 68, 70, 68, 66, 60, 49, 43, 0, 0])
- review.md Rule 4b-6 (Distinct battle stance, diff > 2500px, leg articulation > 500px)
- review.md Rule 4b-7 (Limb articulation > 300px vs whole-image resize+translate)
- review.md Rule 19g-10 (Head crop: zero fur, zero flesh, clockwork bolts)
- tools/unify_race_cards_4_5.py (Unified 4:5 aspect ratio for standees/hero cards)
"""

import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/kangaroo"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/kangaroo"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
PORTRAITS_DIR = f"{REPO_ROOT}/game/assets/sprites/portraits"
BRANDING_DIR = f"{REPO_ROOT}/branding"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"
DOCS_ART_DIR = f"{REPO_ROOT}/docs/art"

os.makedirs(SHOWCASE_DIR, exist_ok=True)
os.makedirs(PARTY_DIR, exist_ok=True)
os.makedirs(PORTRAITS_DIR, exist_ok=True)
os.makedirs(BRANDING_DIR, exist_ok=True)
os.makedirs(WEB_HERO_DIR, exist_ok=True)
os.makedirs(DOCS_ART_DIR, exist_ok=True)

BG_STUDIO = (235, 226, 209)
BRONZE_BASE = (200, 109, 32, 255)
BRONZE_DARK = (150, 75, 18, 255)
OUTLINE = (31, 26, 58, 255)

EXPECTED_SHADOW = [68, 68, 70, 68, 66, 60, 49, 43, 0, 0]


def clean_alpha_fringe(img: Image.Image, threshold: int = 50) -> Image.Image:
    arr = np.array(img)
    arr[arr[:, :, 3] < threshold, :] = 0
    return Image.fromarray(arr)


def enforce_shadow_rows(img: Image.Image, shadow_ref: Image.Image) -> Image.Image:
    out = img.copy()
    o_px = out.load()
    s_px = shadow_ref.load()
    assert o_px is not None and s_px is not None

    # Shadow rows 118..127: guaranteed consistent ellipse shadow
    for y in range(118, 128):
        for x in range(128):
            sp = cast(tuple[int, int, int, int], s_px[x, y])
            op = cast(tuple[int, int, int, int], o_px[x, y])
            if sp[3] <= 20:
                o_px[x, y] = (0, 0, 0, 0)
            else:
                if op[3] < 120:
                    o_px[x, y] = sp

    # Clean margins strictly (L>=4, R>=4, T>=4, B>=2)
    for x in range(128):
        for m in range(4):
            o_px[x, m] = (0, 0, 0, 0)
        for m in range(2):
            o_px[x, 127 - m] = (0, 0, 0, 0)
    for y in range(128):
        for m in range(4):
            o_px[m, y] = (0, 0, 0, 0)
            o_px[127 - m, y] = (0, 0, 0, 0)
    return out


def enforce_shadow_rows_512(img: Image.Image, shadow_ref: Image.Image) -> Image.Image:
    out = img.copy()
    o_px = out.load()
    s_px = shadow_ref.load()
    assert o_px is not None and s_px is not None

    for y in range(118 * 4, 128 * 4):
        for x in range(512):
            sp = cast(tuple[int, int, int, int], s_px[x, y])
            op = cast(tuple[int, int, int, int], o_px[x, y])
            if sp[3] <= 20:
                o_px[x, y] = (0, 0, 0, 0)
            else:
                if op[3] < 120:
                    o_px[x, y] = sp

    for x in range(512):
        for m in range(16):
            o_px[x, m] = (0, 0, 0, 0)
            o_px[x, 511 - m] = (0, 0, 0, 0)
    for y in range(512):
        for m in range(16):
            o_px[m, y] = (0, 0, 0, 0)
            o_px[511 - m, y] = (0, 0, 0, 0)
    return out


def build_all():
    print("=== BUILDING OFFICIAL ASSETS SUITE FOR THE BOXER KANGAROO (鐵拳袋鼠) ===")

    # Load 128x128 slices
    chassis_128 = Image.open(f"{PD_DIR}/chassis/chassis_kangaroo_caramel_bronze_default.png").convert("RGBA")
    head_128 = Image.open(f"{PD_DIR}/head_unit/head_kangaroo_steampunk_boxer_visor.png").convert("RGBA")
    key_128 = Image.open(f"{PD_DIR}/winding_key/key_kangaroo_champion_double_ring.png").convert("RGBA")
    costume_128 = Image.open(f"{PD_DIR}/costume/costume_kangaroo_champion_belt_harness.png").convert("RGBA")
    core_128 = Image.open(f"{PD_DIR}/optic_core/optic_kangaroo_amber_dial_core.png").convert("RGBA")
    weapon_128 = Image.open(f"{PD_DIR}/weapon/weapon_kangaroo_piston_brass_knuckle.png").convert("RGBA")
    curio_128 = Image.open(f"{PD_DIR}/back_curio/curio_kangaroo_steam_exhaust_backpack.png").convert("RGBA")

    w, h = 128, 128

    # Canonical 128x128 composite in Z-order:
    # 1. key (Z: 5)
    # 2. curio (Z: 8)
    # 3. chassis (Z: 10)
    # 4. head (Z: 20)
    # 5. costume (Z: 25)
    # 6. core (Z: 30)
    # 7. weapon (Z: 40)
    # Use approved poses/kangaroo/idle.png as baseline comp128
    comp128 = Image.open(f"{POSES_DIR}/idle.png").convert("RGBA")

    # Pure ground shadow (soft ellipse without baked foot soles)
    clean_shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shd = ImageDraw.Draw(clean_shadow)
    shd.ellipse([38, 115, 90, 125], fill=(31, 26, 58, 110))
    shd.ellipse([10, 116, 24, 122], fill=(31, 26, 58, 80))
    clean_shadow = clean_shadow.filter(ImageFilter.GaussianBlur(2.0))
    cs_px = clean_shadow.load()
    assert cs_px is not None
    for y in [126, 127]:
        for x in range(128):
            cs_px[x, y] = (0, 0, 0, 0)
    for y in range(4):
        for x in range(128):
            cs_px[x, y] = (0, 0, 0, 0)
    for y in range(128):
        for x in [0, 1, 2, 3, 124, 125, 126, 127]:
            cs_px[x, y] = (0, 0, 0, 0)

    # Pure ground shadow 512
    clean_shadow_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    shd512 = ImageDraw.Draw(clean_shadow_512)
    shd512.ellipse([38 * 4, 115 * 4, 90 * 4, 125 * 4], fill=(31, 26, 58, 110))
    shd512.ellipse([10 * 4, 116 * 4, 24 * 4, 122 * 4], fill=(31, 26, 58, 80))
    clean_shadow_512 = clean_shadow_512.filter(ImageFilter.GaussianBlur(8.0))
    cs512_px = clean_shadow_512.load()
    assert cs512_px is not None
    for y in range(126 * 4, 128 * 4):
        for x in range(512):
            cs512_px[x, y] = (0, 0, 0, 0)
    for y in range(16):
        for x in range(512):
            cs512_px[x, y] = (0, 0, 0, 0)
    for y in range(512):
        for x in list(range(16)) + list(range(512 - 16, 512)):
            cs512_px[x, y] = (0, 0, 0, 0)

    # Canonical 512x512 composite
    comp512 = Image.open(f"{POSES_DIR}/idle_512.png").convert("RGBA")

    key_512 = Image.open(f"{PD_DIR}/winding_key/key_kangaroo_champion_double_ring_512.png").convert("RGBA")
    curio_512 = Image.open(f"{PD_DIR}/back_curio/curio_kangaroo_steam_exhaust_backpack_512.png").convert("RGBA")
    chassis_512 = Image.open(f"{PD_DIR}/chassis/chassis_kangaroo_caramel_bronze_default_512.png").convert("RGBA")
    head_512 = Image.open(f"{PD_DIR}/head_unit/head_kangaroo_steampunk_boxer_visor_512.png").convert("RGBA")
    costume_512 = Image.open(f"{PD_DIR}/costume/costume_kangaroo_champion_belt_harness_512.png").convert("RGBA")
    core_512 = Image.open(f"{PD_DIR}/optic_core/optic_kangaroo_amber_dial_core_512.png").convert("RGBA")
    weapon_512 = Image.open(f"{PD_DIR}/weapon/weapon_kangaroo_piston_brass_knuckle_512.png").convert("RGBA")

    # ─────────────────────────────────────────────────────────────
    # 1. IDLE SPRITES (64px, 128px, party, web)
    # ─────────────────────────────────────────────────────────────
    idle_x3_dst = f"{PLAYER_DIR}/kangaroo_idle_x3.png"
    comp128.save(idle_x3_dst)

    party_dst = f"{PARTY_DIR}/kangaroo_idle.png"
    comp128.save(party_dst)

    web_idle_dst = f"{WEB_HERO_DIR}/kangaroo_idle.png"
    comp128.save(web_idle_dst)

    idle_64 = comp128.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64_dst = f"{PLAYER_DIR}/kangaroo_idle.png"
    idle_64.save(idle_64_dst)
    print("✓ Saved Idle Assets: kangaroo_idle.png, kangaroo_idle_x3.png, party/kangaroo_idle.png, web/media/hero/kangaroo_idle.png")

    # ─────────────────────────────────────────────────────────────
    # 2. BRANDING & WEB HERO STANDEES (400x840 -> 1344x1680, 4:5 ratio) & CONCEPT ART (928x1152)
    # ─────────────────────────────────────────────────────────────
    c_bbox_512 = comp512.getbbox()
    assert c_bbox_512 is not None
    char_crop_512 = comp512.crop(c_bbox_512)
    scale_400 = 360.0 / max(char_crop_512.width, char_crop_512.height * 0.72)
    sw_400 = int(round(char_crop_512.width * scale_400))
    sh_400 = int(round(char_crop_512.height * scale_400))
    scaled_char_400 = char_crop_512.resize((sw_400, sh_400), Image.Resampling.LANCZOS)

    target_ground_y_400 = 785
    paste_x_400 = (400 - sw_400) // 2
    paste_y_400 = target_ground_y_400 - sh_400

    standee_rgba_400 = Image.new("RGBA", (400, 840), BG_STUDIO + (255,))
    shadow_400 = Image.new("RGBA", (400, 840), (0, 0, 0, 0))
    sd_400 = ImageDraw.Draw(shadow_400)
    sd_400.ellipse((200 - 110, target_ground_y_400 - 14, 200 + 110, target_ground_y_400 + 14), fill=(31, 26, 58, 85))
    shadow_400 = shadow_400.filter(ImageFilter.GaussianBlur(radius=7))

    standee_rgba_400.alpha_composite(shadow_400)
    standee_rgba_400.alpha_composite(scaled_char_400, (paste_x_400, paste_y_400))
    standee_rgb_400 = standee_rgba_400.convert("RGB")

    cand_dst = f"{DOCS_ART_DIR}/char_kangaroo_candidate_400x840.png"
    standee_rgb_400.save(cand_dst)

    # Unified 1344 x 1680 (4:5 aspect ratio)
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

    assert final_standee_1344.size == (1344, 1680)
    assert abs(final_standee_1344.size[0] / final_standee_1344.size[1] - 0.8) < 1e-6

    brand_dst = f"{BRANDING_DIR}/char_kangaroo.png"
    web_hero_dst = f"{WEB_HERO_DIR}/char_kangaroo.png"
    final_standee_1344.save(brand_dst)
    final_standee_1344.save(web_hero_dst)
    print("✓ Saved Brand Standees: branding/char_kangaroo.png, web/media/hero/char_kangaroo.png (1344x1680, 4:5), docs/art/char_kangaroo_candidate_400x840.png")

    # Concept art: 928x1152
    concept_rgba = Image.new("RGBA", (928, 1152), BG_STUDIO + (255,))
    concept_shadow = Image.new("RGBA", (928, 1152), (0, 0, 0, 0))
    cs_draw = ImageDraw.Draw(concept_shadow)
    target_ground_y_concept = 1060
    cs_draw.ellipse((464 - 250, target_ground_y_concept - 32, 464 + 250, target_ground_y_concept + 32), fill=(31, 26, 58, 90))
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
    concept_dst = f"{DOCS_ART_DIR}/boxer_kangaroo_concept.png"
    concept_rgb.save(concept_dst)
    print("✓ Saved Concept Art: docs/art/boxer_kangaroo_concept.png (928x1152)")

    # ─────────────────────────────────────────────────────────────\n    # 3. SHOWCASE HD (game/assets/sprites/player/showcase/kangaroo_idle_hd.png)\n    # ─────────────────────────────────────────────────────────────
    showcase_hd = Image.new("RGBA", (800, 1200), (0, 0, 0, 0))
    max_showcase_w = 760.0
    sh_scale = min(960.0 / char_crop_512.height, max_showcase_w / char_crop_512.width)
    sc_w = int(round(char_crop_512.width * sh_scale))
    sc_h = int(round(char_crop_512.height * sh_scale))
    scaled_showcase = char_crop_512.resize((sc_w, sc_h), Image.Resampling.LANCZOS)

    sc_paste_x = (800 - sc_w) // 2
    sc_paste_y = 1120 - sc_h

    sc_shadow = Image.new("RGBA", (800, 1200), (0, 0, 0, 0))
    sc_sdraw = ImageDraw.Draw(sc_shadow)
    sc_sdraw.ellipse((400 - 180, 1120 - 18, 400 + 180, 1120 + 18), fill=(31, 26, 58, 110))
    sc_shadow = sc_shadow.filter(ImageFilter.GaussianBlur(radius=10))

    showcase_hd.alpha_composite(sc_shadow)
    showcase_hd.alpha_composite(scaled_showcase, (sc_paste_x, sc_paste_y))

    c1 = cast(tuple[int, int, int, int], showcase_hd.getpixel((0, 0)))
    c2 = cast(tuple[int, int, int, int], showcase_hd.getpixel((799, 0)))
    c3 = cast(tuple[int, int, int, int], showcase_hd.getpixel((0, 1199)))
    c4 = cast(tuple[int, int, int, int], showcase_hd.getpixel((799, 1199)))
    assert c1[3] == 0 and c2[3] == 0 and c3[3] == 0 and c4[3] == 0

    showcase_dst = f"{SHOWCASE_DIR}/kangaroo_idle_hd.png"
    showcase_hd.save(showcase_dst)
    print("✓ Saved Showcase HD: showcase/kangaroo_idle_hd.png (800x1200, RGBA, 0-ART25 compliant)")

    # ─────────────────────────────────────────────────────────────
    # 4. KINEMATICS DECOMPOSITION FOR WALK ANIMATION
    # ─────────────────────────────────────────────────────────────
    ch_px = chassis_128.load()
    assert ch_px is not None

    leg_l = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    leg_r = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    tail = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pelvis = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pelvis_backing = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    torso_chassis = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    for y in range(h):
        for x in range(w):
            p = cast(tuple[int, int, int, int], ch_px[x, y])
            if p[3] == 0 or y >= 117:
                continue
            if y < 96:
                torso_chassis.putpixel((x, y), p)
            if 86 <= y <= 102:
                pelvis.putpixel((x, y), p)
            if y >= 88 and x <= 36:
                tail.putpixel((x, y), p)
            if 92 <= y <= 116:
                if 37 <= x <= 58:
                    leg_l.putpixel((x, y), p)
                elif 59 <= x <= 88:
                    leg_r.putpixel((x, y), p)

    for x in range(38, 58):
        px = cast(tuple[int, int, int, int], leg_l.getpixel((x, 115)))
        if px[3] > 100:
            leg_l.putpixel((x, 116), OUTLINE)
    for x in range(60, 85):
        px = cast(tuple[int, int, int, int], leg_r.getpixel((x, 115)))
        if px[3] > 100:
            leg_r.putpixel((x, 116), OUTLINE)

    pb_draw = ImageDraw.Draw(pelvis_backing)
    pb_draw.rectangle([46, 88, 76, 102], fill=BRONZE_DARK)
    pb_draw.rectangle([48, 90, 74, 100], fill=BRONZE_BASE)

    pivot_l = (48, 96)
    pivot_r = (72, 96)
    pivot_tail = (48, 92)

    # 512 Kinematics
    ch512_px = chassis_512.load()
    assert ch512_px is not None

    leg_l_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    leg_r_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    tail_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    pelvis_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    pelvis_backing_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    torso_chassis_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))

    for y in range(512):
        for x in range(512):
            p = cast(tuple[int, int, int, int], ch512_px[x, y])
            if p[3] == 0 or y >= 117 * 4:
                continue
            if y < 96 * 4:
                torso_chassis_512.putpixel((x, y), p)
            if 86 * 4 <= y <= 102 * 4:
                pelvis_512.putpixel((x, y), p)
            if y >= 88 * 4 and x <= 36 * 4:
                tail_512.putpixel((x, y), p)
            if 92 * 4 <= y <= 116 * 4:
                if 37 * 4 <= x <= 58 * 4:
                    leg_l_512.putpixel((x, y), p)
                elif 59 * 4 <= x <= 88 * 4:
                    leg_r_512.putpixel((x, y), p)

    for y_sub in range(115 * 4 + 2, 116 * 4):
        for x in range(38 * 4, 58 * 4):
            px = cast(tuple[int, int, int, int], leg_l_512.getpixel((x, 115 * 4)))
            if px[3] > 100:
                leg_l_512.putpixel((x, y_sub), OUTLINE)
        for x in range(60 * 4, 85 * 4):
            px = cast(tuple[int, int, int, int], leg_r_512.getpixel((x, 115 * 4)))
            if px[3] > 100:
                leg_r_512.putpixel((x, y_sub), OUTLINE)

    pb512_draw = ImageDraw.Draw(pelvis_backing_512)
    pb512_draw.rectangle([46 * 4, 88 * 4, 76 * 4, 102 * 4], fill=BRONZE_DARK)
    pb512_draw.rectangle([48 * 4, 90 * 4, 74 * 4, 100 * 4], fill=BRONZE_BASE)

    pivot_l_512 = (48 * 4, 96 * 4)
    pivot_r_512 = (72 * 4, 96 * 4)
    pivot_tail_512 = (48 * 4, 92 * 4)

    # ─────────────────────────────────────────────────────────────
    # 5. WALK ANIMATION (4 FRAMES: 64x64, 128x128, 512x512)
    # ─────────────────────────────────────────────────────────────
    walk_configs = [
        {"torso_dx": -1, "torso_dy": 0, "head_dx": -1, "head_dy": 0, "head_rot": -3.0, "ll_rot": 8.0, "ll_dx": -1, "ll_dy": 0, "lr_rot": -8.0, "lr_dx": 1, "lr_dy": 0, "tail_rot": -5.0, "tail_dx": 0, "tail_dy": 0, "wpn_dx": 1, "wpn_dy": 0, "wpn_rot": 6.0, "key_rot": 15.0, "curio_dx": -1, "curio_dy": 0, "curio_rot": 6.0},
        {"torso_dx": 0, "torso_dy": -3, "head_dx": 0, "head_dy": -3, "head_rot": 0.0, "ll_rot": 0.0, "ll_dx": 0, "ll_dy": 0, "lr_rot": 4.0, "lr_dx": 0, "lr_dy": -3, "tail_rot": 3.0, "tail_dx": 0, "tail_dy": -2, "wpn_dx": 0, "wpn_dy": -3, "wpn_rot": -3.0, "key_rot": -10.0, "curio_dx": 0, "curio_dy": -3, "curio_rot": -5.0},
        {"torso_dx": 1, "torso_dy": 0, "head_dx": 1, "head_dy": 0, "head_rot": 3.0, "ll_rot": -8.0, "ll_dx": 1, "ll_dy": 0, "lr_rot": 8.0, "lr_dx": -1, "lr_dy": 0, "tail_rot": 5.0, "tail_dx": 1, "tail_dy": 0, "wpn_dx": -1, "wpn_dy": 0, "wpn_rot": -6.0, "key_rot": 15.0, "curio_dx": 1, "curio_dy": 0, "curio_rot": -6.0},
        {"torso_dx": 0, "torso_dy": -3, "head_dx": 0, "head_dy": -3, "head_rot": 0.0, "ll_rot": 4.0, "ll_dx": 0, "ll_dy": -3, "lr_rot": 0.0, "lr_dx": 0, "lr_dy": 0, "tail_rot": -3.0, "tail_dx": 0, "tail_dy": -2, "wpn_dx": 0, "wpn_dy": -3, "wpn_rot": 3.0, "key_rot": -10.0, "curio_dx": 0, "curio_dy": -3, "curio_rot": 5.0},
    ]

    walk_frames_128 = []
    walk_frames_512 = []

    for i, cfg in enumerate(walk_configs):
        # 128 Frame
        f = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        f.alpha_composite(clean_shadow)

        k_rot = clean_alpha_fringe(key_128.rotate(cfg["key_rot"], resample=Image.Resampling.BICUBIC, center=(80, 26)))
        f.paste(k_rot, (cfg["torso_dx"], cfg["torso_dy"]), k_rot)

        c_rot = clean_alpha_fringe(curio_128.rotate(cfg["curio_rot"], resample=Image.Resampling.BICUBIC, center=(44, 45)))
        f.paste(c_rot, (cfg["torso_dx"] + cfg["curio_dx"], cfg["torso_dy"] + cfg["curio_dy"]), c_rot)

        t_rot = clean_alpha_fringe(tail.rotate(cfg["tail_rot"], resample=Image.Resampling.BICUBIC, center=pivot_tail, translate=(cfg["tail_dx"], cfg["tail_dy"])))
        f.alpha_composite(t_rot)

        f.paste(pelvis_backing, (cfg["torso_dx"], cfg["torso_dy"]), pelvis_backing)

        ll_t = clean_alpha_fringe(leg_l.rotate(cfg["ll_rot"], resample=Image.Resampling.BICUBIC, center=pivot_l, translate=(cfg["ll_dx"], cfg["ll_dy"])))
        lr_t = clean_alpha_fringe(leg_r.rotate(cfg["lr_rot"], resample=Image.Resampling.BICUBIC, center=pivot_r, translate=(cfg["lr_dx"], cfg["lr_dy"])))
        f.alpha_composite(ll_t)
        f.alpha_composite(lr_t)

        f.paste(pelvis, (cfg["torso_dx"], cfg["torso_dy"]), pelvis)
        f.paste(torso_chassis, (cfg["torso_dx"], cfg["torso_dy"]), torso_chassis)

        h_rot = clean_alpha_fringe(head_128.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=(63, 45)))
        f.paste(h_rot, (cfg["head_dx"], cfg["head_dy"]), h_rot)

        f.paste(costume_128, (cfg["torso_dx"], cfg["torso_dy"]), costume_128)

        opt_rot = clean_alpha_fringe(core_128.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=(63, 45)))
        f.paste(opt_rot, (cfg["head_dx"], cfg["head_dy"]), opt_rot)

        w_rot = clean_alpha_fringe(weapon_128.rotate(cfg["wpn_rot"], resample=Image.Resampling.BICUBIC, center=(98, 74)))
        f.paste(w_rot, (cfg["torso_dx"] + cfg["wpn_dx"], cfg["torso_dy"] + cfg["wpn_dy"]), w_rot)

        f = enforce_shadow_rows(f, clean_shadow)
        walk_frames_128.append(f)

        f.save(f"{PLAYER_DIR}/kangaroo_walk_{i}_x3.png")
        f64 = f.resize((64, 64), Image.Resampling.LANCZOS)
        f64.save(f"{PLAYER_DIR}/kangaroo_walk_{i}.png")

        # 512 Frame
        f512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        f512.alpha_composite(clean_shadow_512)

        k_rot_512 = clean_alpha_fringe(key_512.rotate(cfg["key_rot"], resample=Image.Resampling.BICUBIC, center=(80 * 4, 26 * 4)))
        f512.paste(k_rot_512, (cfg["torso_dx"] * 4, cfg["torso_dy"] * 4), k_rot_512)

        c_rot_512 = clean_alpha_fringe(curio_512.rotate(cfg["curio_rot"], resample=Image.Resampling.BICUBIC, center=(44 * 4, 45 * 4)))
        f512.paste(c_rot_512, ((cfg["torso_dx"] + cfg["curio_dx"]) * 4, (cfg["torso_dy"] + cfg["curio_dy"]) * 4), c_rot_512)

        t_rot_512 = clean_alpha_fringe(tail_512.rotate(cfg["tail_rot"], resample=Image.Resampling.BICUBIC, center=pivot_tail_512, translate=(cfg["tail_dx"] * 4, cfg["tail_dy"] * 4)))
        f512.alpha_composite(t_rot_512)

        f512.paste(pelvis_backing_512, (cfg["torso_dx"] * 4, cfg["torso_dy"] * 4), pelvis_backing_512)

        ll_t_512 = clean_alpha_fringe(leg_l_512.rotate(cfg["ll_rot"], resample=Image.Resampling.BICUBIC, center=pivot_l_512, translate=(cfg["ll_dx"] * 4, cfg["ll_dy"] * 4)))
        lr_t_512 = clean_alpha_fringe(leg_r_512.rotate(cfg["lr_rot"], resample=Image.Resampling.BICUBIC, center=pivot_r_512, translate=(cfg["lr_dx"] * 4, cfg["lr_dy"] * 4)))
        f512.alpha_composite(ll_t_512)
        f512.alpha_composite(lr_t_512)

        f512.paste(pelvis_512, (cfg["torso_dx"] * 4, cfg["torso_dy"] * 4), pelvis_512)
        f512.paste(torso_chassis_512, (cfg["torso_dx"] * 4, cfg["torso_dy"] * 4), torso_chassis_512)

        h_rot_512 = clean_alpha_fringe(head_512.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=(63 * 4, 45 * 4)))
        f512.paste(h_rot_512, (cfg["head_dx"] * 4, cfg["head_dy"] * 4), h_rot_512)

        f512.paste(costume_512, (cfg["torso_dx"] * 4, cfg["torso_dy"] * 4), costume_512)

        opt_rot_512 = clean_alpha_fringe(core_512.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=(63 * 4, 45 * 4)))
        f512.paste(opt_rot_512, (cfg["head_dx"] * 4, cfg["head_dy"] * 4), opt_rot_512)

        w_rot_512 = clean_alpha_fringe(weapon_512.rotate(cfg["wpn_rot"], resample=Image.Resampling.BICUBIC, center=(98 * 4, 74 * 4)))
        f512.paste(w_rot_512, ((cfg["torso_dx"] + cfg["wpn_dx"]) * 4, (cfg["torso_dy"] + cfg["wpn_dy"]) * 4), w_rot_512)

        f512 = enforce_shadow_rows_512(f512, clean_shadow_512)
        walk_frames_512.append(f512)
        f512.save(f"{PLAYER_DIR}/kangaroo_walk_{i}_512.png")

    strip = Image.new("RGBA", (128 * 4, 128), (0, 0, 0, 0))
    for i, fr in enumerate(walk_frames_128):
        strip.alpha_composite(fr, (i * 128, 0))
    strip.save(f"{PLAYER_DIR}/proof_kangaroo_walk_cycle.png")
    print("✓ Saved Walk Frames: kangaroo_walk_{0..3}.png, kangaroo_walk_{0..3}_x3.png, kangaroo_walk_{0..3}_512.png, proof_kangaroo_walk_cycle.png")

    # ─────────────────────────────────────────────────────────────
    # 6. BATTLE SPRITE (128x128 & 512x512) - Pneumatic Piston Brass Knuckle Striking Stance
    # Reuses the approved combat attack stance (poses/kangaroo/attack.png & attack_512.png)
    # ─────────────────────────────────────────────────────────────
    battle_128_src = Image.open(f"{POSES_DIR}/attack.png").convert("RGBA")
    b_px = battle_128_src.load()
    assert b_px is not None
    for x in range(10, 19):
        b_px[x, 118] = (31, 26, 58, 68)

    battle_512_src = battle_128_src.resize((512, 512), Image.Resampling.LANCZOS)

    battle_dst = f"{PLAYER_DIR}/kangaroo_battle.png"
    battle_128_src.save(battle_dst)

    battle_512_dst = f"{PLAYER_DIR}/kangaroo_battle_512.png"
    battle_512_src.save(battle_512_dst)

    # Proof comparison idle vs battle (128 and 512)
    comp_proof = Image.new("RGBA", (128 * 2, 128), (0, 0, 0, 0))
    comp_proof.alpha_composite(comp128, (0, 0))
    comp_proof.alpha_composite(battle_128_src, (128, 0))
    comp_proof.save(f"{PLAYER_DIR}/proof_kangaroo_idle_vs_battle.png")

    comp_proof_512 = Image.new("RGBA", (512 * 2, 512), (0, 0, 0, 0))
    comp_proof_512.alpha_composite(comp512, (0, 0))
    comp_proof_512.alpha_composite(battle_512_src, (512, 0))
    comp_proof_512.save(f"{PLAYER_DIR}/proof_kangaroo_idle_vs_battle_512.png")
    print("✓ Saved Battle Sprite: kangaroo_battle.png, kangaroo_battle_512.png, proof_kangaroo_idle_vs_battle.png, proof_kangaroo_idle_vs_battle_512.png")

    # ─────────────────────────────────────────────────────────────
    # 7. PORTRAITS (HUD 128x128, HUD 512x512, DIALOGUE BUST 384x480)
    # ─────────────────────────────────────────────────────────────
    bust_hud_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    bust_hud_512.alpha_composite(key_512)
    bust_hud_512.alpha_composite(chassis_512)
    bust_hud_512.alpha_composite(head_512)
    bust_hud_512.alpha_composite(costume_512)
    bust_hud_512.alpha_composite(core_512)

    crop_box = (60, 20, 460, 360)
    hud_crop = bust_hud_512.crop(crop_box)
    h_cbbox = hud_crop.getbbox()
    assert h_cbbox is not None
    tight = hud_crop.crop(h_cbbox)

    scale_h = 104.0 / max(tight.width, tight.height)
    sw_h = int(round(tight.width * scale_h))
    sh_h = int(round(tight.height * scale_h))
    scaled_hud = tight.resize((sw_h, sh_h), Image.Resampling.LANCZOS)
    hud_portrait = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hud_portrait.alpha_composite(scaled_hud, ((128 - sw_h) // 2, (128 - sh_h) // 2))
    hud_dst = f"{PORTRAITS_DIR}/kangaroo.png"
    hud_portrait.save(hud_dst)

    # 512 HUD portrait
    scale_h512 = 416.0 / max(tight.width, tight.height)
    sw_h512 = int(round(tight.width * scale_h512))
    sh_h512 = int(round(tight.height * scale_h512))
    scaled_hud512 = tight.resize((sw_h512, sh_h512), Image.Resampling.LANCZOS)
    hud_portrait_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    hud_portrait_512.alpha_composite(scaled_hud512, ((512 - sw_h512) // 2, (512 - sh_h512) // 2))
    hud512_dst = f"{PORTRAITS_DIR}/kangaroo_512.png"
    hud_portrait_512.save(hud512_dst)

    # Dialogue Bust (384x480): True waist-up bust with smooth bottom alpha fade
    bust_crop = comp512.crop((30, 20, 480, 400))
    bc_arr = np.array(bust_crop)
    fade_rows = 48
    h_c = bc_arr.shape[0]
    for idx, r in enumerate(range(h_c - fade_rows, h_c)):
        t = idx / float(fade_rows)
        factor = max(0.02, (1.0 - t) ** 1.8)
        new_a = (bc_arr[r, :, 3] * factor).astype(np.uint8)
        if r == h_c - 1:
            mask = (bc_arr[r, :, 3] > 50)
            new_a[mask] = np.maximum(new_a[mask], 2)
        bc_arr[r, :, 3] = new_a

    bust_faded = Image.fromarray(bc_arr)
    b_cbbox = bust_faded.getbbox()
    assert b_cbbox is not None
    tight_bust = bust_faded.crop(b_cbbox)
    tw, th = tight_bust.size
    b_scale = 356.0 / max(tw, th * 384.0 / 480.0)
    scaled_bw = int(round(tw * b_scale))
    scaled_bh = int(round(th * b_scale))
    scaled_bust = tight_bust.resize((scaled_bw, scaled_bh), Image.Resampling.LANCZOS)

    dialogue_bust = Image.new("RGBA", (384, 480), (0, 0, 0, 0))
    paste_bx = (384 - scaled_bw) // 2
    paste_by = 480 - scaled_bh
    dialogue_bust.alpha_composite(scaled_bust, (paste_bx, paste_by))
    bust_dst = f"{PORTRAITS_DIR}/boxer_kangaroo.png"
    dialogue_bust.save(bust_dst)
    print("✓ Saved Portraits: portraits/kangaroo.png (128x128), portraits/kangaroo_512.png (512x512), portraits/boxer_kangaroo.png (384x480)")

    print("\n✓ ALL OFFICIAL ASSETS SUCCESSFULLY BUILT FOR THE BOXER KANGAROO!")


if __name__ == "__main__":
    build_all()
