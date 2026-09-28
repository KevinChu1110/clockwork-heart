#!/usr/bin/env python3
"""
build_official_assets_courser.py
Builds the complete official asset suite for the 37th race: 鐵蹄駿駒 (The Ironhoof Courser, courser).
Conforms to:
- Task t_71f0de7e specification
- docs/design/paperdoll_slots.json
- review.md 0-ART25 (showcase/*_idle_hd.png RGBA mode and 4-corner alpha=0 check)
- review.md 0-ART26 (No cross-race borrowing, only use canonical courser slices)
- review.md 0-ART18 (Zero fur, zero flesh, clean margins, mechanical joints)
- review.md Rule 4b-4 (Non-translation walk kinematics)
- review.md Rule 4b-5 (Consistent ground contact shadow across all frames: [34, 34, 34, 34, 0, 0, 0, 0, 0, 0])
- review.md Rule 4b-6 (Distinct battle stance, diff > 2500px, leg/body articulation > 500px)
- review.md Rule 4b-7 (Limb/segment articulation > 300px vs whole-image resize+translate)
- review.md Rule 19g-10 (Head crop: zero fur, zero flesh, clockwork bolts)
- tools/unify_race_cards_4_5.py (Unified 4:5 aspect ratio for standees/hero cards)
"""

import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/courser"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/courser"
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
OUTLINE = (31, 26, 58, 255)

EXPECTED_SHADOW = [34, 34, 34, 34, 0, 0, 0, 0, 0, 0]


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
            if sp[3] <= 20:
                o_px[x, y] = (0, 0, 0, 0)
            else:
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
            if sp[3] <= 20:
                o_px[x, y] = (0, 0, 0, 0)
            else:
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
    print("=== BUILDING OFFICIAL ASSETS SUITE FOR THE IRONHOOF COURSER (鐵蹄駿駒) ===")

    # Load 128x128 slices
    chassis_128 = Image.open(f"{PD_DIR}/chassis/chassis_courser_cream_gold_default.png").convert("RGBA")
    head_128 = Image.open(f"{PD_DIR}/head_unit/head_courser_brass_chanfron_mane.png").convert("RGBA")
    key_128 = Image.open(f"{PD_DIR}/winding_key/key_courser_baroque_trefoil_gold.png").convert("RGBA")
    costume_128 = Image.open(f"{PD_DIR}/costume/costume_courser_dawn_patrol_cuirass.png").convert("RGBA")
    core_128 = Image.open(f"{PD_DIR}/optic_core/face_courser_sapphire_optic_lens.png").convert("RGBA")
    weapon_128 = Image.open(f"{PD_DIR}/weapon/weapon_courser_cavalry_saber.png").convert("RGBA")
    curio_128 = Image.open(f"{PD_DIR}/back_curio/curio_courser_articulated_spring_tail.png").convert("RGBA")

    w, h = 128, 128

    # Approved poses/courser/idle.png as baseline comp128
    comp128 = Image.open(f"{POSES_DIR}/idle.png").convert("RGBA")
    comp512 = Image.open(f"{POSES_DIR}/idle_512.png").convert("RGBA")

    # Extract exact ground shadow
    clean_shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    c_px = comp128.load()
    s_px = clean_shadow.load()
    assert c_px is not None and s_px is not None
    for y in range(118, 128):
        for x in range(128):
            p = cast(tuple[int, int, int, int], c_px[x, y])
            if p[3] > 20:
                s_px[x, y] = p

    clean_shadow_512 = clean_shadow.resize((512, 512), Image.Resampling.LANCZOS)

    # ─────────────────────────────────────────────────────────────
    # 1. IDLE SPRITES (64px, 128px, party, web)
    # ─────────────────────────────────────────────────────────────
    idle_x3_dst = f"{PLAYER_DIR}/courser_idle_x3.png"
    comp128.save(idle_x3_dst)

    party_dst = f"{PARTY_DIR}/courser_idle.png"
    comp128.save(party_dst)

    web_idle_dst = f"{WEB_HERO_DIR}/courser_idle.png"
    comp128.save(web_idle_dst)

    idle_64 = comp128.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64_dst = f"{PLAYER_DIR}/courser_idle.png"
    idle_64.save(idle_64_dst)
    print("✓ Saved Idle Assets: courser_idle.png, courser_idle_x3.png, party/courser_idle.png, web/media/hero/courser_idle.png")

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
    sd_400.ellipse((200 - 120, target_ground_y_400 - 15, 200 + 120, target_ground_y_400 + 15), fill=(31, 26, 58, 85))
    shadow_400 = shadow_400.filter(ImageFilter.GaussianBlur(radius=7))

    standee_rgba_400.alpha_composite(shadow_400)
    standee_rgba_400.alpha_composite(scaled_char_400, (paste_x_400, paste_y_400))
    standee_rgb_400 = standee_rgba_400.convert("RGB")

    cand_dst = f"{DOCS_ART_DIR}/char_courser_candidate_400x840.png"
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

    brand_dst = f"{BRANDING_DIR}/char_courser.png"
    web_hero_dst = f"{WEB_HERO_DIR}/char_courser.png"
    final_standee_1344.save(brand_dst)
    final_standee_1344.save(web_hero_dst)
    print("✓ Saved Brand Standees: branding/char_courser.png, web/media/hero/char_courser.png (1344x1680, 4:5), docs/art/char_courser_candidate_400x840.png")

    # Concept art: 928x1152
    concept_rgba = Image.new("RGBA", (928, 1152), BG_STUDIO + (255,))
    concept_shadow = Image.new("RGBA", (928, 1152), (0, 0, 0, 0))
    cs_draw = ImageDraw.Draw(concept_shadow)
    target_ground_y_concept = 1060
    cs_draw.ellipse((464 - 260, target_ground_y_concept - 34, 464 + 260, target_ground_y_concept + 34), fill=(31, 26, 58, 90))
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
    concept_dst = f"{DOCS_ART_DIR}/ironhoof_courser_concept.png"
    concept_rgb.save(concept_dst)
    print("✓ Saved Concept Art: docs/art/ironhoof_courser_concept.png (928x1152)")

    # ─────────────────────────────────────────────────────────────
    # 3. SHOWCASE HD (game/assets/sprites/player/showcase/courser_idle_hd.png)
    # ─────────────────────────────────────────────────────────────
    showcase_hd = Image.new("RGBA", (800, 1200), (0, 0, 0, 0))
    max_showcase_w = 720.0
    sh_scale = min(920.0 / char_crop_512.height, max_showcase_w / char_crop_512.width)
    sc_w = int(round(char_crop_512.width * sh_scale))
    sc_h = int(round(char_crop_512.height * sh_scale))
    scaled_showcase = char_crop_512.resize((sc_w, sc_h), Image.Resampling.LANCZOS)

    sc_paste_x = (800 - sc_w) // 2
    sc_paste_y = 1120 - sc_h

    sc_shadow = Image.new("RGBA", (800, 1200), (0, 0, 0, 0))
    sc_sdraw = ImageDraw.Draw(sc_shadow)
    sc_sdraw.ellipse((400 - 190, 1120 - 20, 400 + 190, 1120 + 20), fill=(31, 26, 58, 110))
    sc_shadow = sc_shadow.filter(ImageFilter.GaussianBlur(radius=10))

    showcase_hd.alpha_composite(sc_shadow)
    showcase_hd.alpha_composite(scaled_showcase, (sc_paste_x, sc_paste_y))

    c1 = cast(tuple[int, int, int, int], showcase_hd.getpixel((0, 0)))
    c2 = cast(tuple[int, int, int, int], showcase_hd.getpixel((799, 0)))
    c3 = cast(tuple[int, int, int, int], showcase_hd.getpixel((0, 1199)))
    c4 = cast(tuple[int, int, int, int], showcase_hd.getpixel((799, 1199)))
    assert c1[3] == 0 and c2[3] == 0 and c3[3] == 0 and c4[3] == 0

    showcase_dst = f"{SHOWCASE_DIR}/courser_idle_hd.png"
    showcase_hd.save(showcase_dst)
    print("✓ Saved Showcase HD: showcase/courser_idle_hd.png (800x1200, RGBA, 0-ART25 compliant)")

    # ─────────────────────────────────────────────────────────────
    # 4. KINEMATICS DECOMPOSITION FOR WALK ANIMATION
    # ─────────────────────────────────────────────────────────────
    ch_px = chassis_128.load()
    assert ch_px is not None

    leg_l = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    leg_r = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pelvis = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    torso_chassis = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    for y in range(h):
        for x in range(w):
            p = cast(tuple[int, int, int, int], ch_px[x, y])
            if p[3] == 0 or y >= 118:
                continue
            if y < 94:
                torso_chassis.putpixel((x, y), p)
            if 88 <= y <= 104 and 42 <= x <= 86:
                pelvis.putpixel((x, y), p)
            if 96 <= y <= 117:
                if x <= 62:
                    leg_l.putpixel((x, y), p)
                else:
                    leg_r.putpixel((x, y), p)

    pivot_l = (50, 100)
    pivot_r = (78, 100)
    pivot_head = (64, 35)
    pivot_key = (88, 35)
    pivot_wpn = (96, 50)
    pivot_curio = (36, 85)

    walk_configs = [
        # Frame 0: Left stride forward, cavalry saber lowered forward, mane wave
        {
            "torso_dx": -1, "torso_dy": 0, "torso_rot": -2.0,
            "head_dx": -1, "head_dy": 0, "head_rot": -2.0,
            "ll_rot": 8.0, "ll_dx": -1, "ll_dy": 0,
            "lr_rot": -8.0, "lr_dx": 1, "lr_dy": 0,
            "wpn_dx": -1, "wpn_dy": 1, "wpn_rot": 4.0,
            "key_rot": 18.0,
            "curio_rot": -5.0, "curio_dx": -1, "curio_dy": 0,
        },
        # Frame 1: Center stride compression (passing stance, spring tail recoil)
        {
            "torso_dx": 0, "torso_dy": -2, "torso_rot": 0.0,
            "head_dx": 0, "head_dy": -2, "head_rot": 0.0,
            "ll_rot": 0.0, "ll_dx": 0, "ll_dy": 0,
            "lr_rot": 4.0, "lr_dx": 0, "lr_dy": -2,
            "wpn_dx": 0, "wpn_dy": -2, "wpn_rot": -2.0,
            "key_rot": -12.0,
            "curio_rot": 4.0, "curio_dx": 0, "curio_dy": -2,
        },
        # Frame 2: Right stride forward, cavalry saber raised, mane & tail sway
        {
            "torso_dx": 1, "torso_dy": 0, "torso_rot": 2.0,
            "head_dx": 1, "head_dy": 0, "head_rot": 2.0,
            "ll_rot": -8.0, "ll_dx": 1, "ll_dy": 0,
            "lr_rot": 8.0, "lr_dx": -1, "lr_dy": 0,
            "wpn_dx": 2, "wpn_dy": -1, "wpn_rot": -4.0,
            "key_rot": 18.0,
            "curio_rot": 5.0, "curio_dx": 1, "curio_dy": 0,
        },
        # Frame 3: Rebound float / spring tail lift
        {
            "torso_dx": 0, "torso_dy": -3, "torso_rot": 0.0,
            "head_dx": 0, "head_dy": -3, "head_rot": 0.0,
            "ll_rot": 4.0, "ll_dx": 0, "ll_dy": -2,
            "lr_rot": 0.0, "lr_dx": 0, "lr_dy": 0,
            "wpn_dx": 0, "wpn_dy": -3, "wpn_rot": 2.0,
            "key_rot": -12.0,
            "curio_rot": -3.0, "curio_dx": 0, "curio_dy": -2,
        },
    ]

    # ─────────────────────────────────────────────────────────────
    # 5. WALK ANIMATION (4 FRAMES: 64x64, 128x128, 512x512)
    # ─────────────────────────────────────────────────────────────
    walk_frames_128 = []
    walk_frames_512 = []

    for i, cfg in enumerate(walk_configs):
        # 128 Frame
        f = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        f.alpha_composite(clean_shadow)

        # 1. key (winding key behind chassis, z=5)
        k_rot = clean_alpha_fringe(key_128.rotate(cfg["key_rot"], resample=Image.Resampling.BICUBIC, center=pivot_key))
        f.paste(k_rot, (cfg["torso_dx"], cfg["torso_dy"]), k_rot)

        # 2. back curio (spring tail, z=8)
        c_rot = clean_alpha_fringe(curio_128.rotate(cfg["curio_rot"], resample=Image.Resampling.BICUBIC, center=pivot_curio, translate=(cfg["curio_dx"], cfg["curio_dy"])))
        f.alpha_composite(c_rot)

        # 3. legs
        ll_t = clean_alpha_fringe(leg_l.rotate(cfg["ll_rot"], resample=Image.Resampling.BICUBIC, center=pivot_l, translate=(cfg["ll_dx"], cfg["ll_dy"])))
        lr_t = clean_alpha_fringe(leg_r.rotate(cfg["lr_rot"], resample=Image.Resampling.BICUBIC, center=pivot_r, translate=(cfg["lr_dx"], cfg["lr_dy"])))
        f.alpha_composite(ll_t)
        f.alpha_composite(lr_t)

        # 4. pelvis
        f.paste(pelvis, (cfg["torso_dx"], cfg["torso_dy"]), pelvis)

        # 5. torso chassis (z=10)
        tc_rot = clean_alpha_fringe(torso_chassis.rotate(cfg["torso_rot"], resample=Image.Resampling.BICUBIC, center=(64, 70), translate=(cfg["torso_dx"], cfg["torso_dy"])))
        f.alpha_composite(tc_rot)

        # 6. head unit (z=20)
        h_rot = clean_alpha_fringe(head_128.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=pivot_head, translate=(cfg["head_dx"], cfg["head_dy"])))
        f.alpha_composite(h_rot)

        # 7. costume (z=25)
        f.paste(costume_128, (cfg["torso_dx"], cfg["torso_dy"]), costume_128)

        # 8. optic core (z=30)
        opt_rot = clean_alpha_fringe(core_128.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=pivot_head, translate=(cfg["head_dx"], cfg["head_dy"])))
        f.alpha_composite(opt_rot)

        # 9. weapon (z=40)
        w_rot = clean_alpha_fringe(weapon_128.rotate(cfg["wpn_rot"], resample=Image.Resampling.BICUBIC, center=pivot_wpn, translate=(cfg["torso_dx"] + cfg["wpn_dx"], cfg["torso_dy"] + cfg["wpn_dy"])))
        f.alpha_composite(w_rot)

        f = enforce_shadow_rows(f, clean_shadow)
        walk_frames_128.append(f)

        f.save(f"{PLAYER_DIR}/courser_walk_{i}_x3.png")
        f64 = f.resize((64, 64), Image.Resampling.LANCZOS)
        f64.save(f"{PLAYER_DIR}/courser_walk_{i}.png")

        # 512 Frame (LANCZOS upscale + shadow enforce)
        f512 = f.resize((512, 512), Image.Resampling.LANCZOS)
        f512 = enforce_shadow_rows_512(f512, clean_shadow_512)
        walk_frames_512.append(f512)
        f512.save(f"{PLAYER_DIR}/courser_walk_{i}_512.png")

    strip = Image.new("RGBA", (128 * 4, 128), (0, 0, 0, 0))
    for i, fr in enumerate(walk_frames_128):
        strip.alpha_composite(fr, (i * 128, 0))
    strip.save(f"{PLAYER_DIR}/proof_courser_walk_cycle.png")
    print("✓ Saved Walk Frames: courser_walk_{0..3}.png, courser_walk_{0..3}_x3.png, courser_walk_{0..3}_512.png, proof_courser_walk_cycle.png")

    # ─────────────────────────────────────────────────────────────
    # 6. BATTLE SPRITE (128x128 & 512x512) - Dawn Cavalry Saber Thrust Stance
    # Reuses the approved combat attack stance (poses/courser/attack.png & attack_512.png)
    # ─────────────────────────────────────────────────────────────
    battle_128_src = Image.open(f"{POSES_DIR}/attack.png").convert("RGBA")
    battle_512_src = Image.open(f"{POSES_DIR}/attack_512.png").convert("RGBA")

    battle_dst = f"{PLAYER_DIR}/courser_battle.png"
    battle_128_src.save(battle_dst)

    battle_512_dst = f"{PLAYER_DIR}/courser_battle_512.png"
    battle_512_src.save(battle_512_dst)

    # Proof comparison idle vs battle (128 and 512)
    comp_proof = Image.new("RGBA", (128 * 2, 128), (0, 0, 0, 0))
    comp_proof.alpha_composite(comp128, (0, 0))
    comp_proof.alpha_composite(battle_128_src, (128, 0))
    comp_proof.save(f"{PLAYER_DIR}/proof_courser_idle_vs_battle.png")

    comp_proof_512 = Image.new("RGBA", (512 * 2, 512), (0, 0, 0, 0))
    comp_proof_512.alpha_composite(comp512, (0, 0))
    comp_proof_512.alpha_composite(battle_512_src, (512, 0))
    comp_proof_512.save(f"{PLAYER_DIR}/proof_courser_idle_vs_battle_512.png")

    print("✓ Saved Battle Sprite: courser_battle.png, courser_battle_512.png, proof_courser_idle_vs_battle.png, proof_courser_idle_vs_battle_512.png")

    # ─────────────────────────────────────────────────────────────
    # 7. PORTRAITS (HUD 128x128, HUD 512x512, DIALOGUE BUST 384x480)
    # ─────────────────────────────────────────────────────────────
    # Head & chanfron box from comp512
    crop_box = (100, 10, 440, 240)
    hud_crop = comp512.crop(crop_box)
    h_cbbox = hud_crop.getbbox()
    assert h_cbbox is not None
    tight = hud_crop.crop(h_cbbox)

    # HUD 128x128
    scale_h = 104.0 / max(tight.width, tight.height)
    sw_h = int(round(tight.width * scale_h))
    sh_h = int(round(tight.height * scale_h))
    scaled_hud = tight.resize((sw_h, sh_h), Image.Resampling.LANCZOS)
    hud_portrait = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hud_portrait.alpha_composite(scaled_hud, ((128 - sw_h) // 2, (128 - sh_h) // 2))
    hud_dst = f"{PORTRAITS_DIR}/courser.png"
    hud_portrait.save(hud_dst)

    # HUD 512x512
    scale_h512 = 416.0 / max(tight.width, tight.height)
    sw_h512 = int(round(tight.width * scale_h512))
    sh_h512 = int(round(tight.height * scale_h512))
    scaled_hud512 = tight.resize((sw_h512, sh_h512), Image.Resampling.LANCZOS)
    hud_portrait_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    hud_portrait_512.alpha_composite(scaled_hud512, ((512 - sw_h512) // 2, (512 - sh_h512) // 2))
    hud512_dst = f"{PORTRAITS_DIR}/courser_512.png"
    hud_portrait_512.save(hud512_dst)

    # Dialogue Bust (384x480): True waist-up bust with smooth bottom alpha fade
    bust_crop = comp512.crop((50, 10, 480, 400))
    bc_arr = np.array(bust_crop)
    fade_rows = 50
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
    bust_dst = f"{PORTRAITS_DIR}/ironhoof_courser.png"
    dialogue_bust.save(bust_dst)
    print("✓ Saved Portraits: portraits/courser.png (128x128), portraits/courser_512.png (512x512), portraits/ironhoof_courser.png (384x480)")

    print("\n✓ ALL OFFICIAL ASSETS SUCCESSFULLY BUILT FOR THE IRONHOOF COURSER!")


if __name__ == "__main__":
    build_all()
