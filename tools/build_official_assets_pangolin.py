#!/usr/bin/env python3
"""
build_official_assets_pangolin.py
Builds the complete official asset suite for the 18th race: 沙鱗穿山甲 (The Dune Pangolin, pangolin).
Conforms to:
- Task t_4a34f692 specification
- docs/design/DUNE_PANGOLIN_DESIGN_PROPOSAL.md
- docs/design/paperdoll_slots.json
- review.md 0-ART25 (showcase/*_idle_hd.png RGBA mode and 4-corner alpha=0 check)
- review.md 0-ART26 (No cross-race borrowing, only use canonical pangolin slices)
- review.md 0-ART18 (Zero fur, zero flesh, clean margins, mechanical joints)
- review.md 0-MKT7 (Single-wield dune-drill claw on right hand)
- review.md Rule 4b-4 (Non-translation walk kinematics)
- review.md Rule 4b-5 (Consistent ground contact shadow across all frames)
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
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/pangolin"
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

def enforce_shadow_rows(img: Image.Image, baseline: Image.Image) -> Image.Image:
    out = img.copy()
    o_px = out.load()
    s_px = baseline.load()
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
    return out

def enforce_shadow_rows_512(img: Image.Image, baseline: Image.Image) -> Image.Image:
    out = img.copy()
    o_px = out.load()
    s_px = baseline.load()
    assert o_px is not None and s_px is not None
    for y in range(118 * 4, 128 * 4):
        for x in range(512):
            sp = cast(tuple[int, int, int, int], s_px[x, y])
            fp = cast(tuple[int, int, int, int], o_px[x, y])
            if sp[3] <= 20:
                if fp[3] > 20:
                    o_px[x, y] = (0, 0, 0, 0)
            else:
                if fp[3] <= 20:
                    o_px[x, y] = sp
    return out

def build_all():
    print("=== BUILDING OFFICIAL ASSETS SUITE FOR DUNE PANGOLIN ===")

    # Load 128x128 slices
    chassis_128 = Image.open(f"{PD_DIR}/chassis/chassis_pangolin_dune_orange_default.png").convert("RGBA")
    head_128 = Image.open(f"{PD_DIR}/head_unit/head_pangolin_brass_acoustic_ears.png").convert("RGBA")
    key_128 = Image.open(f"{PD_DIR}/winding_key/key_pangolin_coil_scale_spiral_gold.png").convert("RGBA")
    costume_128 = Image.open(f"{PD_DIR}/costume/costume_pangolin_scavenger_tinker_vest.png").convert("RGBA")
    core_128 = Image.open(f"{PD_DIR}/optic_core/face_pangolin_sky_blue_optic_domes.png").convert("RGBA")
    weapon_128 = Image.open(f"{PD_DIR}/weapon/weapon_pangolin_dune_drill_claw.png").convert("RGBA")
    curio_128 = Image.open(f"{PD_DIR}/back_curio/curio_pangolin_segmented_scale_tail.png").convert("RGBA")

    w, h = 128, 128

    # Canonical 128x128 composite in Z-order:
    # key (z=5) -> curio (z=8) -> chassis (z=10) -> head (z=20) -> costume (z=25) -> core (z=30) -> weapon (z=40)
    comp128 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    comp128.alpha_composite(key_128)
    comp128.alpha_composite(curio_128)
    comp128.alpha_composite(chassis_128)
    comp128.alpha_composite(head_128)
    comp128.alpha_composite(costume_128)
    comp128.alpha_composite(core_128)
    comp128.alpha_composite(weapon_128)

    # Clean ground contact shadow reference from comp128
    clean_shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cs_px = clean_shadow.load()
    c_px = comp128.load()
    assert cs_px is not None and c_px is not None
    for y in range(118, 128):
        for x in range(128):
            p = cast(tuple[int, int, int, int], c_px[x, y])
            if p[3] > 20:
                cs_px[x, y] = p

    # Canonical 512x512 composite
    key_512 = Image.open(f"{PD_DIR}/winding_key/key_pangolin_coil_scale_spiral_gold_512.png").convert("RGBA")
    curio_512 = Image.open(f"{PD_DIR}/back_curio/curio_pangolin_segmented_scale_tail_512.png").convert("RGBA")
    chassis_512 = Image.open(f"{PD_DIR}/chassis/chassis_pangolin_dune_orange_default_512.png").convert("RGBA")
    head_512 = Image.open(f"{PD_DIR}/head_unit/head_pangolin_brass_acoustic_ears_512.png").convert("RGBA")
    core_512 = Image.open(f"{PD_DIR}/optic_core/face_pangolin_sky_blue_optic_domes_512.png").convert("RGBA")
    costume_512 = Image.open(f"{PD_DIR}/costume/costume_pangolin_scavenger_tinker_vest_512.png").convert("RGBA")
    weapon_512 = Image.open(f"{PD_DIR}/weapon/weapon_pangolin_dune_drill_claw_512.png").convert("RGBA")

    comp512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    comp512.alpha_composite(key_512)
    comp512.alpha_composite(curio_512)
    comp512.alpha_composite(chassis_512)
    comp512.alpha_composite(head_512)
    comp512.alpha_composite(costume_512)
    comp512.alpha_composite(core_512)
    comp512.alpha_composite(weapon_512)

    clean_shadow_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    cs512_px = clean_shadow_512.load()
    c512_px = comp512.load()
    assert cs512_px is not None and c512_px is not None
    for y in range(118 * 4, 128 * 4):
        for x in range(512):
            p = cast(tuple[int, int, int, int], c512_px[x, y])
            if p[3] > 20:
                cs512_px[x, y] = p

    # ─────────────────────────────────────────────────────────────
    # 1. IDLE SPRITES (64px, 128px, party, web)
    # ─────────────────────────────────────────────────────────────
    idle_x3_dst = f"{PLAYER_DIR}/pangolin_idle_x3.png"
    comp128.save(idle_x3_dst)

    party_dst = f"{PARTY_DIR}/pangolin_idle.png"
    comp128.save(party_dst)

    web_idle_dst = f"{WEB_HERO_DIR}/pangolin_idle.png"
    comp128.save(web_idle_dst)

    idle_64 = comp128.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64_dst = f"{PLAYER_DIR}/pangolin_idle.png"
    idle_64.save(idle_64_dst)
    print("✓ Saved Idle Assets: pangolin_idle.png, pangolin_idle_x3.png, party/pangolin_idle.png, web/media/hero/pangolin_idle.png")

    # ─────────────────────────────────────────────────────────────
    # 2. BRANDING & WEB HERO STANDEES (400x840 -> 1344x1680, 4:5 ratio) & CONCEPT ART (928x1152)
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
    sd_400.ellipse((200 - 110, target_ground_y_400 - 14, 200 + 110, target_ground_y_400 + 14), fill=(31, 26, 58, 85))
    shadow_400 = shadow_400.filter(ImageFilter.GaussianBlur(radius=7))

    standee_rgba_400.alpha_composite(shadow_400)
    standee_rgba_400.alpha_composite(scaled_char_400, (paste_x_400, paste_y_400))
    standee_rgb_400 = standee_rgba_400.convert("RGB")

    cand_dst = f"{DOCS_ART_DIR}/char_pangolin_candidate_400x840.png"
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

    brand_dst = f"{BRANDING_DIR}/char_pangolin.png"
    web_hero_dst = f"{WEB_HERO_DIR}/char_pangolin.png"
    final_standee_1344.save(brand_dst)
    final_standee_1344.save(web_hero_dst)
    print("✓ Saved Brand Standees: branding/char_pangolin.png, web/media/hero/char_pangolin.png (1344x1680, 4:5), docs/art/char_pangolin_candidate_400x840.png")

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
    concept_dst = f"{DOCS_ART_DIR}/dune_pangolin_concept.png"
    concept_rgb.save(concept_dst)
    print("✓ Saved Concept Art: docs/art/dune_pangolin_concept.png (928x1152)")

    # ─────────────────────────────────────────────────────────────
    # 3. SHOWCASE HD (game/assets/sprites/player/showcase/pangolin_idle_hd.png)
    # ─────────────────────────────────────────────────────────────
    showcase_hd = Image.new("RGBA", (800, 1200), (0, 0, 0, 0))
    sh_scale = 1000.0 / char_crop_512.height
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

    showcase_dst = f"{SHOWCASE_DIR}/pangolin_idle_hd.png"
    showcase_hd.save(showcase_dst)
    print("✓ Saved Showcase HD: showcase/pangolin_idle_hd.png (800x1200, RGBA, 0-ART25 compliant)")

    # ─────────────────────────────────────────────────────────────
    # 4. KINEMATICS DECOMPOSITION FOR WALK & BATTLE
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
            if y >= 115 and p[3] < 180 and p[0] < 45 and p[1] < 40 and p[2] < 75:
                continue
            if y < 98:
                torso_chassis.putpixel((x, y), p)
            if y >= 88:
                if x <= 62:
                    leg_l.putpixel((x, y), p)
                elif x >= 65:
                    leg_r.putpixel((x, y), p)

    pivot_l = (52, 94)
    pivot_r = (75, 94)

    # 512 Kinematics components
    ch512_px = chassis_512.load()
    assert ch512_px is not None

    leg_l_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    leg_r_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    torso_chassis_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))

    for y in range(512):
        for x in range(512):
            p = cast(tuple[int, int, int, int], ch512_px[x, y])
            if p[3] == 0:
                continue
            if y >= 115 * 4 and p[3] < 180 and p[0] < 45 and p[1] < 40 and p[2] < 75:
                continue
            if y < 98 * 4:
                torso_chassis_512.putpixel((x, y), p)
            if y >= 88 * 4:
                if x <= 62 * 4:
                    leg_l_512.putpixel((x, y), p)
                elif x >= 65 * 4:
                    leg_r_512.putpixel((x, y), p)

    pivot_l_512 = (52 * 4, 94 * 4)
    pivot_r_512 = (75 * 4, 94 * 4)

    # ─────────────────────────────────────────────────────────────
    # 5. WALK ANIMATION (4 FRAMES: 64x64, 128x128, 512x512)
    # ─────────────────────────────────────────────────────────────
    walk_configs = [
        {"torso_dy": 0, "torso_dx": 0, "ll_rot": 10.0, "ll_dx": -2, "ll_dy": 0, "lr_rot": -10.0, "lr_dx": 2, "lr_dy": 0, "wpn_dy": 1, "wpn_dx": 0, "key_rot": 6.0, "curio_dy": 0, "curio_rot": 4.0},
        {"torso_dy": -2, "torso_dx": 0, "ll_rot": -2.0, "ll_dx": 0, "ll_dy": -1, "lr_rot": 14.0, "lr_dx": -1, "lr_dy": -3, "wpn_dy": -2, "wpn_dx": 1, "key_rot": -6.0, "curio_dy": -1, "curio_rot": -6.0},
        {"torso_dy": 0, "torso_dx": 0, "ll_rot": -10.0, "ll_dx": 2, "ll_dy": 0, "lr_rot": 10.0, "lr_dx": -2, "lr_dy": 0, "wpn_dy": 1, "wpn_dx": 0, "key_rot": 6.0, "curio_dy": 0, "curio_rot": 4.0},
        {"torso_dy": -2, "torso_dx": 0, "ll_rot": 14.0, "ll_dx": 1, "ll_dy": -3, "lr_rot": -2.0, "lr_dx": 0, "lr_dy": -1, "wpn_dy": -2, "wpn_dx": -1, "key_rot": -6.0, "curio_dy": -1, "curio_rot": -6.0},
    ]

    walk_frames_128 = []
    walk_frames_512 = []

    for i, cfg in enumerate(walk_configs):
        # 128 Frame
        f = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        f.alpha_composite(clean_shadow)
        k_rot = key_128.rotate(cfg["key_rot"], resample=Image.Resampling.BICUBIC, center=(83, 40))
        f.paste(k_rot, (cfg["torso_dx"], cfg["torso_dy"]), k_rot)
        c_rot = curio_128.rotate(cfg["curio_rot"], resample=Image.Resampling.BICUBIC, center=(33, 94))
        f.paste(c_rot, (cfg["torso_dx"], cfg["torso_dy"] + cfg["curio_dy"]), c_rot)
        ll_t = leg_l.rotate(cfg["ll_rot"], resample=Image.Resampling.BICUBIC, center=pivot_l, translate=(cfg["ll_dx"], cfg["ll_dy"]))
        lr_t = leg_r.rotate(cfg["lr_rot"], resample=Image.Resampling.BICUBIC, center=pivot_r, translate=(cfg["lr_dx"], cfg["lr_dy"]))
        f.alpha_composite(ll_t)
        f.alpha_composite(lr_t)
        f.paste(torso_chassis, (cfg["torso_dx"], cfg["torso_dy"]), torso_chassis)
        f.paste(head_128, (cfg["torso_dx"], cfg["torso_dy"]), head_128)
        f.paste(core_128, (cfg["torso_dx"], cfg["torso_dy"]), core_128)
        f.paste(costume_128, (cfg["torso_dx"], cfg["torso_dy"]), costume_128)
        f.paste(weapon_128, (cfg["torso_dx"] + cfg["wpn_dx"], cfg["torso_dy"] + cfg["wpn_dy"]), weapon_128)

        f = enforce_shadow_rows(f, comp128)
        walk_frames_128.append(f)

        f.save(f"{PLAYER_DIR}/pangolin_walk_{i}_x3.png")
        f64 = f.resize((64, 64), Image.Resampling.LANCZOS)
        f64.save(f"{PLAYER_DIR}/pangolin_walk_{i}.png")

        # 512 Frame
        f512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        f512.alpha_composite(clean_shadow_512)
        k_rot_512 = key_512.rotate(cfg["key_rot"], resample=Image.Resampling.BICUBIC, center=(83 * 4, 40 * 4))
        f512.paste(k_rot_512, (cfg["torso_dx"] * 4, cfg["torso_dy"] * 4), k_rot_512)
        c_rot_512 = curio_512.rotate(cfg["curio_rot"], resample=Image.Resampling.BICUBIC, center=(33 * 4, 94 * 4))
        f512.paste(c_rot_512, (cfg["torso_dx"] * 4, (cfg["torso_dy"] + cfg["curio_dy"]) * 4), c_rot_512)
        ll_t_512 = leg_l_512.rotate(cfg["ll_rot"], resample=Image.Resampling.BICUBIC, center=pivot_l_512, translate=(cfg["ll_dx"] * 4, cfg["ll_dy"] * 4))
        lr_t_512 = leg_r_512.rotate(cfg["lr_rot"], resample=Image.Resampling.BICUBIC, center=pivot_r_512, translate=(cfg["lr_dx"] * 4, cfg["lr_dy"] * 4))
        f512.alpha_composite(ll_t_512)
        f512.alpha_composite(lr_t_512)
        f512.paste(torso_chassis_512, (cfg["torso_dx"] * 4, cfg["torso_dy"] * 4), torso_chassis_512)
        f512.paste(head_512, (cfg["torso_dx"] * 4, cfg["torso_dy"] * 4), head_512)
        f512.paste(core_512, (cfg["torso_dx"] * 4, cfg["torso_dy"] * 4), core_512)
        f512.paste(costume_512, (cfg["torso_dx"] * 4, cfg["torso_dy"] * 4), costume_512)
        f512.paste(weapon_512, ((cfg["torso_dx"] + cfg["wpn_dx"]) * 4, (cfg["torso_dy"] + cfg["wpn_dy"]) * 4), weapon_512)

        f512 = enforce_shadow_rows_512(f512, comp512)
        walk_frames_512.append(f512)
        f512.save(f"{PLAYER_DIR}/pangolin_walk_{i}_512.png")

    strip = Image.new("RGBA", (128 * 4, 128), (0, 0, 0, 0))
    for i, fr in enumerate(walk_frames_128):
        strip.alpha_composite(fr, (i * 128, 0))
    strip.save(f"{PLAYER_DIR}/proof_pangolin_walk_cycle.png")
    print("✓ Saved Walk Frames: pangolin_walk_{0..3}.png, pangolin_walk_{0..3}_x3.png, pangolin_walk_{0..3}_512.png, proof_pangolin_walk_cycle.png")

    # ─────────────────────────────────────────────────────────────
    # 6. BATTLE SPRITE (128x128 & 512x512) - Monk Grounded Break-Shield Drill Stance
    # ─────────────────────────────────────────────────────────────
    b_torso_dx = 1
    b_torso_dy = 2

    ll_b = leg_l.rotate(-15.0, resample=Image.Resampling.BICUBIC, center=pivot_l, translate=(-3, 1))
    lr_b = leg_r.rotate(18.0, resample=Image.Resampling.BICUBIC, center=pivot_r, translate=(3, 1))

    torso_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    torso_b.paste(torso_chassis, (b_torso_dx, b_torso_dy), torso_chassis)

    head_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    head_b.paste(head_128, (b_torso_dx + 1, b_torso_dy), head_128)

    costume_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    costume_b.paste(costume_128, (b_torso_dx, b_torso_dy), costume_128)

    core_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    core_b.paste(core_128, (b_torso_dx + 1, b_torso_dy), core_b)

    key_b = key_128.rotate(22.0, resample=Image.Resampling.BICUBIC, center=(83, 40), translate=(b_torso_dx + 1, b_torso_dy - 1))
    curio_b = curio_128.rotate(-14.0, resample=Image.Resampling.BICUBIC, center=(33, 94), translate=(b_torso_dx - 3, b_torso_dy + 1))
    wpn_b = weapon_128.rotate(-20.0, resample=Image.Resampling.BICUBIC, center=(92, 78), translate=(b_torso_dx + 5, b_torso_dy - 4))

    battle_sprite = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    battle_sprite.alpha_composite(clean_shadow)
    battle_sprite.alpha_composite(key_b)
    battle_sprite.alpha_composite(curio_b)
    battle_sprite.alpha_composite(ll_b)
    battle_sprite.alpha_composite(lr_b)
    battle_sprite.alpha_composite(torso_b)
    battle_sprite.alpha_composite(head_b)
    battle_sprite.alpha_composite(core_b)
    battle_sprite.alpha_composite(costume_b)
    battle_sprite.alpha_composite(wpn_b)

    battle_sprite = enforce_shadow_rows(battle_sprite, comp128)
    battle_dst = f"{PLAYER_DIR}/pangolin_battle.png"
    battle_sprite.save(battle_dst)

    # 512 Battle sprite
    ll_b_512 = leg_l_512.rotate(-15.0, resample=Image.Resampling.BICUBIC, center=pivot_l_512, translate=(-3 * 4, 1 * 4))
    lr_b_512 = leg_r_512.rotate(18.0, resample=Image.Resampling.BICUBIC, center=pivot_r_512, translate=(3 * 4, 1 * 4))

    torso_b_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    torso_b_512.paste(torso_chassis_512, (b_torso_dx * 4, b_torso_dy * 4), torso_chassis_512)

    head_b_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    head_b_512.paste(head_512, ((b_torso_dx + 1) * 4, b_torso_dy * 4), head_512)

    costume_b_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    costume_b_512.paste(costume_512, (b_torso_dx * 4, b_torso_dy * 4), costume_512)

    core_b_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    core_b_512.paste(core_512, ((b_torso_dx + 1) * 4, b_torso_dy * 4), core_b_512)

    key_b_512 = key_512.rotate(22.0, resample=Image.Resampling.BICUBIC, center=(83 * 4, 40 * 4), translate=((b_torso_dx + 1) * 4, (b_torso_dy - 1) * 4))
    curio_b_512 = curio_512.rotate(-14.0, resample=Image.Resampling.BICUBIC, center=(33 * 4, 94 * 4), translate=((b_torso_dx - 3) * 4, (b_torso_dy + 1) * 4))
    wpn_b_512 = weapon_512.rotate(-20.0, resample=Image.Resampling.BICUBIC, center=(92 * 4, 78 * 4), translate=((b_torso_dx + 5) * 4, (b_torso_dy - 4) * 4))

    battle_sprite_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    battle_sprite_512.alpha_composite(clean_shadow_512)
    battle_sprite_512.alpha_composite(key_b_512)
    battle_sprite_512.alpha_composite(curio_b_512)
    battle_sprite_512.alpha_composite(ll_b_512)
    battle_sprite_512.alpha_composite(lr_b_512)
    battle_sprite_512.alpha_composite(torso_b_512)
    battle_sprite_512.alpha_composite(head_b_512)
    battle_sprite_512.alpha_composite(core_b_512)
    battle_sprite_512.alpha_composite(costume_b_512)
    battle_sprite_512.alpha_composite(wpn_b_512)

    battle_sprite_512 = enforce_shadow_rows_512(battle_sprite_512, comp512)
    battle_512_dst = f"{PLAYER_DIR}/pangolin_battle_512.png"
    battle_sprite_512.save(battle_512_dst)

    # Proof comparison idle vs battle (128 and 512)
    comp_proof = Image.new("RGBA", (128 * 2, 128), (0, 0, 0, 0))
    comp_proof.alpha_composite(comp128, (0, 0))
    comp_proof.alpha_composite(battle_sprite, (128, 0))
    comp_proof.save(f"{PLAYER_DIR}/proof_pangolin_idle_vs_battle.png")

    comp_proof_512 = Image.new("RGBA", (512 * 2, 512), (0, 0, 0, 0))
    comp_proof_512.alpha_composite(comp512, (0, 0))
    comp_proof_512.alpha_composite(battle_sprite_512, (512, 0))
    comp_proof_512.save(f"{PLAYER_DIR}/proof_pangolin_idle_vs_battle_512.png")
    print("✓ Saved Battle Sprite: pangolin_battle.png, pangolin_battle_512.png, proof_pangolin_idle_vs_battle.png, proof_pangolin_idle_vs_battle_512.png")

    # ─────────────────────────────────────────────────────────────
    # 7. PORTRAITS (HUD 128x128, HUD 512x512, DIALOGUE BUST 384x480)
    # ─────────────────────────────────────────────────────────────
    # HUD portrait (128x128 & 512x512): focused head & collar avatar bust
    bust_hud_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    bust_hud_512.alpha_composite(key_512)
    bust_hud_512.alpha_composite(chassis_512)
    bust_hud_512.alpha_composite(head_512)
    bust_hud_512.alpha_composite(costume_512)
    bust_hud_512.alpha_composite(core_512)

    crop_box = (50, 20, 460, 320)
    hud_crop = bust_hud_512.crop(crop_box)
    tight = hud_crop.crop(hud_crop.getbbox())
    scale_h = 104.0 / max(tight.width, tight.height)
    sw_h = int(round(tight.width * scale_h))
    sh_h = int(round(tight.height * scale_h))
    scaled_hud = tight.resize((sw_h, sh_h), Image.Resampling.LANCZOS)
    hud_portrait = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hud_portrait.alpha_composite(scaled_hud, ((128 - sw_h) // 2, (128 - sh_h) // 2))
    hud_dst = f"{PORTRAITS_DIR}/pangolin.png"
    hud_portrait.save(hud_dst)

    # 512 HUD portrait
    scale_h512 = 416.0 / max(tight.width, tight.height)
    sw_h512 = int(round(tight.width * scale_h512))
    sh_h512 = int(round(tight.height * scale_h512))
    scaled_hud512 = tight.resize((sw_h512, sh_h512), Image.Resampling.LANCZOS)
    hud_portrait_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    hud_portrait_512.alpha_composite(scaled_hud512, ((512 - sw_h512) // 2, (512 - sh_h512) // 2))
    hud512_dst = f"{PORTRAITS_DIR}/pangolin_512.png"
    hud_portrait_512.save(hud512_dst)

    # Dialogue bust (384x480): proper waist-up bust anchored to bottom
    bust_crop = comp512.crop((35, 35, 465, 420))
    bc_arr = np.array(bust_crop)
    fade_rows = 12
    h_c = bc_arr.shape[0]
    for idx, r in enumerate(range(h_c - fade_rows, h_c)):
        factor = 1.0 - (idx / fade_rows) * 0.3
        bc_arr[r, :, 3] = (bc_arr[r, :, 3] * factor).astype(np.uint8)
    bust_faded = Image.fromarray(bc_arr)
    tight_bust = bust_faded.crop(bust_faded.getbbox())
    tw, th = tight_bust.size
    b_scale = 352.0 / tw
    scaled_bw = int(round(tw * b_scale))
    scaled_bh = int(round(th * b_scale))
    scaled_bust = tight_bust.resize((scaled_bw, scaled_bh), Image.Resampling.LANCZOS)
    dialogue_bust = Image.new("RGBA", (384, 480), (0, 0, 0, 0))
    paste_bx = (384 - scaled_bw) // 2
    paste_by = 480 - scaled_bh
    dialogue_bust.alpha_composite(scaled_bust, (paste_bx, paste_by))
    bust_dst = f"{PORTRAITS_DIR}/dune_pangolin.png"
    dialogue_bust.save(bust_dst)
    print("✓ Saved Portraits: portraits/pangolin.png (128x128), portraits/pangolin_512.png (512x512), portraits/dune_pangolin.png (384x480)")

    print("\n✓ ALL OFFICIAL ASSETS SUCCESSFULLY BUILT FOR DUNE PANGOLIN!")

if __name__ == "__main__":
    build_all()
