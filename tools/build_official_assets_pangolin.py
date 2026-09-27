#!/usr/bin/env python3
"""
build_official_assets_pangolin.py
Builds the complete official asset suite for the 18th race: 沙鱗穿山甲 (The Dune Pangolin, pangolin).
Conforms to:
- Task t_ea828ac6 specification
- docs/design/DUNE_PANGOLIN_DESIGN_PROPOSAL.md
- docs/design/paperdoll_slots.json
- review.md 0-ART25 (showcase/*_idle_hd.png RGBA mode and 4-corner alpha=0 check)
- review.md 0-ART26 (No cross-race borrowing, only use canonical pangolin slices)
- review.md 0-ART18 (Zero fur, zero flesh, clean margins, mechanical joints)
- review.md 0-MKT7 (Single-wield dune-drill claw on right hand)
- tools/unify_race_cards_4_5.py (Unified 4:5 aspect ratio for standees/hero cards)
"""

import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter
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
    print("✓ Saved Brand Standees: branding/char_pangolin.png, web/media/hero/char_pangolin.png (1344x1680, 4:5)")

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
    # 4. PORTRAITS (HUD 128x128 & DIALOGUE BUST 384x480)
    # ─────────────────────────────────────────────────────────────
    # HUD portrait (128x128): focused head & collar avatar bust
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

    # Dialogue bust (384x480): proper waist-up bust anchored to bottom
    ch_bust_arr = np.array(chassis_512)
    for y in range(320, 512):
        for x in range(512):
            if y > 380:
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

    bust_crop = bust_dialogue_512.crop((20, 15, 490, 380))
    bw, bh = bust_crop.size
    b_scale = 360.0 / bw
    scaled_bw = int(round(bw * b_scale))
    scaled_bh = int(round(bh * b_scale))
    scaled_bust = bust_crop.resize((scaled_bw, scaled_bh), Image.Resampling.LANCZOS)
    dialogue_bust = Image.new("RGBA", (384, 480), (0, 0, 0, 0))
    paste_bx = (384 - scaled_bw) // 2
    paste_by = 480 - scaled_bh
    dialogue_bust.alpha_composite(scaled_bust, (paste_bx, paste_by))
    bust_dst = f"{PORTRAITS_DIR}/dune_pangolin.png"
    dialogue_bust.save(bust_dst)
    print("✓ Saved Portraits: portraits/pangolin.png (128x128), portraits/dune_pangolin.png (384x480)")

    print("\n✓ ALL OFFICIAL ASSETS SUCCESSFULLY BUILT FOR DUNE PANGOLIN!")

if __name__ == "__main__":
    build_all()
