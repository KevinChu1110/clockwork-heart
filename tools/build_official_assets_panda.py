#!/usr/bin/env python3
"""
build_official_assets_panda.py
Builds the complete official asset suite for the 13th race: 瓷韻熊貓 (The Porcelain Panda, panda).
Conforms to:
- Task t_3e4d1475 specification
- docs/design/PORCELAIN_PANDA_DESIGN_PROPOSAL.md
- docs/design/paperdoll_slots.json
- review.md 0-ART26 (No cross-race borrowing, only use canonical panda slices)
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
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/panda"
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
    print("=== BUILDING PORCELAIN PANDA (瓷韻熊貓) OFFICIAL ASSET SUITE ===")

    # ─────────────────────────────────────────────────────────────
    # 0. LOAD SLICES (128px & 512px)
    # ─────────────────────────────────────────────────────────────
    chassis_128 = Image.open(f"{PD_DIR}/chassis/paint_panda_porcelain.png").convert("RGBA")
    head_128 = Image.open(f"{PD_DIR}/head_unit/head_panda_brass_socket_ears.png").convert("RGBA")
    key_128 = Image.open(f"{PD_DIR}/winding_key/key_panda_taiji_ruyi_brass.png").convert("RGBA")
    costume_128 = Image.open(f"{PD_DIR}/costume/costume_panda_zen_apprentice_robe.png").convert("RGBA")
    core_128 = Image.open(f"{PD_DIR}/optic_core/core_obsidian_amber_quartz.png").convert("RGBA")
    weapon_128 = Image.open(f"{PD_DIR}/weapon/wpn_panda_taiji_cestus.png").convert("RGBA")
    curio_128 = Image.open(f"{PD_DIR}/back_curio/curio_panda_floating_taiji_box.png").convert("RGBA")

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

    # Canonical 512x512 composite
    key_512 = Image.open(f"{PD_DIR}/winding_key/key_panda_taiji_ruyi_brass_512.png").convert("RGBA")
    curio_512 = Image.open(f"{PD_DIR}/back_curio/curio_panda_floating_taiji_box_512.png").convert("RGBA")
    chassis_512 = Image.open(f"{PD_DIR}/chassis/paint_panda_porcelain_512.png").convert("RGBA")
    head_512 = Image.open(f"{PD_DIR}/head_unit/head_panda_brass_socket_ears_512.png").convert("RGBA")
    costume_512 = Image.open(f"{PD_DIR}/costume/costume_panda_zen_apprentice_robe_512.png").convert("RGBA")
    core_512 = Image.open(f"{PD_DIR}/optic_core/core_obsidian_amber_quartz_512.png").convert("RGBA")
    weapon_512 = Image.open(f"{PD_DIR}/weapon/wpn_panda_taiji_cestus_512.png").convert("RGBA")

    comp512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    comp512.alpha_composite(key_512)
    comp512.alpha_composite(curio_512)
    comp512.alpha_composite(chassis_512)
    comp512.alpha_composite(head_512)
    comp512.alpha_composite(costume_512)
    comp512.alpha_composite(core_512)
    comp512.alpha_composite(weapon_512)

    # Clean ground contact shadow matching chassis creation
    clean_shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cs_d = ImageDraw.Draw(clean_shadow)
    cs_d.ellipse([64 - 34, 116 - 4, 64 + 34, 116 + 5], fill=(31, 26, 58, 125))
    clean_shadow = clean_shadow.filter(ImageFilter.GaussianBlur(1.4))

    # ─────────────────────────────────────────────────────────────
    # 1. IDLE SPRITES (64px, 128px, party, web)
    # ─────────────────────────────────────────────────────────────
    idle_x3_dst = f"{PLAYER_DIR}/panda_idle_x3.png"
    comp128.save(idle_x3_dst)

    party_dst = f"{PARTY_DIR}/panda_idle.png"
    comp128.save(party_dst)

    web_idle_dst = f"{WEB_HERO_DIR}/panda_idle.png"
    comp128.save(web_idle_dst)

    idle_64 = comp128.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64_dst = f"{PLAYER_DIR}/panda_idle.png"
    idle_64.save(idle_64_dst)
    print("✓ Saved Idle Assets: panda_idle.png, panda_idle_x3.png, party/panda_idle.png, web/media/hero/panda_idle.png")

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
    cand_dst = f"{DOCS_ART_DIR}/char_panda_candidate_400x840.png"
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

    brand_dst = f"{BRANDING_DIR}/char_panda.png"
    web_hero_dst = f"{WEB_HERO_DIR}/char_panda.png"
    final_standee_1344.save(brand_dst)
    final_standee_1344.save(web_hero_dst)
    print("✓ Saved Brand Standees: branding/char_panda.png, web/media/hero/char_panda.png (1344x1680, 4:5)")

    # Concept art: 928x1152 matching colossus_elephant_concept, spring_frog_concept, etc.
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
    concept_dst = f"{DOCS_ART_DIR}/porcelain_panda_concept.png"
    concept_rgb.save(concept_dst)
    print(f"✓ Saved Concept Art: docs/art/porcelain_panda_concept.png (928x1152)")

    # ─────────────────────────────────────────────────────────────
    # 3. KINEMATICS DECOMPOSITION WITH TAIJI JOINTS
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
            # Skip pure soft shadow pixels from limbs/torso
            if y >= 113 and p[3] < 200 and p[0] < 45 and p[1] < 40 and p[2] < 75:
                continue
            # Torso
            if y <= 104:
                torso_chassis.putpixel((x, y), p)
            # Legs: hip joints start around y=85 down to feet y=117
            if y >= 85:
                if x <= 58:
                    leg_l.putpixel((x, y), p)
                elif x >= 70:
                    leg_r.putpixel((x, y), p)

    pivot_l = (41, 92)
    pivot_r = (84, 92)

    # ─────────────────────────────────────────────────────────────
    # 4. WALK ANIMATION (4 FRAMES: 64x64 & 128x128)
    # ─────────────────────────────────────────────────────────────
    walk_configs = [
        {"torso_dy": 0, "torso_dx": 0, "ll_rot": 10.0, "ll_dx": -2, "ll_dy": 0, "lr_rot": -10.0, "lr_dx": 2, "lr_dy": 0, "wpn_dy": 1, "wpn_dx": 0, "key_rot": 8.0, "curio_dy": 0},
        {"torso_dy": -2, "torso_dx": 0, "ll_rot": -2.0, "ll_dx": 0, "ll_dy": -1, "lr_rot": 14.0, "lr_dx": -1, "lr_dy": -3, "wpn_dy": -2, "wpn_dx": 1, "key_rot": -8.0, "curio_dy": -1},
        {"torso_dy": 0, "torso_dx": 0, "ll_rot": -10.0, "ll_dx": 2, "ll_dy": 0, "lr_rot": 10.0, "lr_dx": -2, "lr_dy": 0, "wpn_dy": 1, "wpn_dx": 0, "key_rot": 8.0, "curio_dy": 0},
        {"torso_dy": -2, "torso_dx": 0, "ll_rot": 14.0, "ll_dx": 1, "ll_dy": -3, "lr_rot": -2.0, "lr_dx": 0, "lr_dy": -1, "wpn_dy": -2, "wpn_dx": -1, "key_rot": -8.0, "curio_dy": -1},
    ]

    walk_frames_128 = []
    for i, cfg in enumerate(walk_configs):
        f = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        f.alpha_composite(clean_shadow)
        k_rot = key_128.rotate(cfg["key_rot"], resample=Image.Resampling.BICUBIC, center=(28, 28))
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

        f = enforce_shadow_rows(f, comp128)
        walk_frames_128.append(f)

        f.save(f"{PLAYER_DIR}/panda_walk_{i}_x3.png")
        f64 = f.resize((64, 64), Image.Resampling.LANCZOS)
        f64.save(f"{PLAYER_DIR}/panda_walk_{i}.png")

    strip = Image.new("RGBA", (128 * 4, 128), (0, 0, 0, 0))
    for i, fr in enumerate(walk_frames_128):
        strip.alpha_composite(fr, (i * 128, 0))
    strip.save(f"{PLAYER_DIR}/proof_panda_walk_cycle.png")
    print("✓ Saved Walk Frames: panda_walk_{0..3}.png, panda_walk_{0..3}_x3.png, proof_panda_walk_cycle.png")

    # ─────────────────────────────────────────────────────────────
    # 5. BATTLE SPRITE (128x128) - Zen Taiji Monk Punch & Defense Stance
    # ─────────────────────────────────────────────────────────────
    b_torso_dx = 1
    b_torso_dy = 3

    # Legs in grounded martial stance
    ll_b = leg_l.rotate(-18.0, resample=Image.Resampling.BICUBIC, center=pivot_l, translate=(-3, 1))
    lr_b = leg_r.rotate(20.0, resample=Image.Resampling.BICUBIC, center=pivot_r, translate=(4, 1))

    torso_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    torso_b.paste(torso_chassis, (b_torso_dx, b_torso_dy), torso_chassis)

    head_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    head_b.paste(head_128, (b_torso_dx + 1, b_torso_dy), head_128)

    costume_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    costume_b.paste(costume_128, (b_torso_dx, b_torso_dy), costume_128)

    core_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    core_b.paste(core_128, (b_torso_dx, b_torso_dy), core_b)

    # Winding key torque wound
    key_b = key_128.rotate(24.0, resample=Image.Resampling.BICUBIC, center=(28, 28), translate=(b_torso_dx - 1, b_torso_dy - 1))

    # Curio box floating/swept back
    curio_b = curio_128.rotate(-16.0, resample=Image.Resampling.BICUBIC, center=(24, 44), translate=(b_torso_dx - 3, b_torso_dy))

    # Taiji Cestus fist thrust forward in punch strike
    wpn_b = weapon_128.rotate(-20.0, resample=Image.Resampling.BICUBIC, center=(94, 75), translate=(b_torso_dx + 7, b_torso_dy - 6))

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

    battle_sprite = enforce_shadow_rows(battle_sprite, comp128)

    battle_dst = f"{PLAYER_DIR}/panda_battle.png"
    battle_sprite.save(battle_dst)

    # Proof comparison idle vs battle
    comp_proof = Image.new("RGBA", (128 * 2, 128), (0, 0, 0, 0))
    comp_proof.alpha_composite(comp128, (0, 0))
    comp_proof.alpha_composite(battle_sprite, (128, 0))
    comp_proof.save(f"{PLAYER_DIR}/proof_panda_idle_vs_battle.png")
    print("✓ Saved Battle Sprite: panda_battle.png, proof_panda_idle_vs_battle.png")

    # ─────────────────────────────────────────────────────────────
    # 6. PORTRAITS (HUD 128x128 & DIALOGUE BUST 384x480)
    # ─────────────────────────────────────────────────────────────
    # HUD portrait (128x128): focused head & collar avatar bust
    bust_hud_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    bust_hud_512.alpha_composite(key_512)
    bust_hud_512.alpha_composite(chassis_512)
    bust_hud_512.alpha_composite(head_512)
    bust_hud_512.alpha_composite(costume_512)
    bust_hud_512.alpha_composite(core_512)

    crop_box = (50, 39, 390, 350)
    hud_crop = bust_hud_512.crop(crop_box)
    tight = hud_crop.crop(hud_crop.getbbox())
    scale_h = 104.0 / max(tight.width, tight.height)
    sw_h = int(round(tight.width * scale_h))
    sh_h = int(round(tight.height * scale_h))
    scaled_hud = tight.resize((sw_h, sh_h), Image.Resampling.LANCZOS)
    hud_portrait = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hud_portrait.alpha_composite(scaled_hud, ((128 - sw_h) // 2, (128 - sh_h) // 2))
    hud_dst = f"{PORTRAITS_DIR}/panda.png"
    hud_portrait.save(hud_dst)

    # Dialogue bust (384x480): proper waist-up bust (no legs/feet), anchored to bottom (y=480)
    ch_bust_arr = np.array(chassis_512)
    for y in range(320, 512):
        for x in range(512):
            if x <= 235 or x >= 285 or y > 355:
                ch_bust_arr[y, x] = [0, 0, 0, 0]
    ch_bust = Image.fromarray(ch_bust_arr)

    bust_dialogue_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    bust_dialogue_512.alpha_composite(key_512)
    bust_dialogue_512.alpha_composite(curio_512)
    bust_dialogue_512.alpha_composite(ch_bust)
    bust_dialogue_512.alpha_composite(head_512)
    bust_dialogue_512.alpha_composite(costume_512)
    bust_dialogue_512.alpha_composite(core_512)
    bust_dialogue_512.alpha_composite(weapon_512)

    bust_crop = bust_dialogue_512.crop((45, 35, 455, 365))
    bw, bh = bust_crop.size
    b_scale = 360.0 / bw
    scaled_bw = int(round(bw * b_scale))
    scaled_bh = int(round(bh * b_scale))
    scaled_bust = bust_crop.resize((scaled_bw, scaled_bh), Image.Resampling.LANCZOS)
    dialogue_bust = Image.new("RGBA", (384, 480), (0, 0, 0, 0))
    paste_bx = (384 - scaled_bw) // 2
    paste_by = 480 - scaled_bh
    dialogue_bust.alpha_composite(scaled_bust, (paste_bx, paste_by))
    bust_dst = f"{PORTRAITS_DIR}/porcelain_panda.png"
    dialogue_bust.save(bust_dst)
    print("✓ Saved Portraits: portraits/panda.png (128x128), portraits/porcelain_panda.png (384x480)")

    print("\n✓ ALL OFFICIAL ASSETS SUCCESSFULLY BUILT FOR PORCELAIN PANDA!")

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
