#!/usr/bin/env python3
"""
build_official_assets_crane_bear.py
Builds official asset suites for:
- 第七種族 雲嵐鶴 (The Cloud Crane, crane)
- 第八種族 玄軸熊 (The Iron Bear, bear)
Conforms to:
- tiger-official-assets (commit 215f8ac) standards
- docs/art/CLOUD_CRANE_DESIGN_PROPOSAL.md
- docs/art/IRON_BEAR_DESIGN_PROPOSAL.md
- docs/world/CANON.md
- art_direction.md 15-item checklist
"""

import os
from typing import cast
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

REPO_ROOT = "/opt/side/bravesoul-game"
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

def build_crane():
    print("=== BUILDING CLOUD CRANE (雲嵐鶴) OFFICIAL ASSETS ===")
    crane_pd = f"{PLAYER_DIR}/paperdoll/crane"
    comp_path = f"{crane_pd}/proof_paperdoll_crane_composite.png"
    assert os.path.exists(comp_path), f"Missing {comp_path}"
    comp = Image.open(comp_path).convert("RGBA")

    # 1. Standee & Candidate (400x840)
    # Source high-res cutout: /tmp/crane_cut_all.png (center character at X=560..869, Y=85..724)
    cutout_all = Image.open("/tmp/crane_cut_all.png").convert("RGBA")
    char_crop = cutout_all.crop((560, 85, 870, 725))
    
    # Save high-res concept
    if os.path.exists("/tmp/crane_concept_green.png"):
        concept = Image.open("/tmp/crane_concept_green.png")
        concept_dst = f"{DOCS_ART_DIR}/cloud_crane_concept.png"
        concept.save(concept_dst)
        print(f"  ✓ Saved {concept_dst}")

    # Scale character so width is ~360px (leaving 20px margins each side)
    scale = 360.0 / char_crop.width
    sw = int(round(char_crop.width * scale))
    sh = int(round(char_crop.height * scale))
    scaled_char = char_crop.resize((sw, sh), Image.Resampling.LANCZOS)

    standee_rgba = Image.new("RGBA", (400, 840), BG_STUDIO + (255,))
    paste_x = (400 - sw) // 2
    target_ground_y = 785
    paste_y = target_ground_y - sh

    # Contact shadow
    shadow_img = Image.new("RGBA", (400, 840), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_img)
    s_draw.ellipse((200 - 80, target_ground_y - 12, 200 + 80, target_ground_y + 12), fill=(31, 26, 58, 80))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=6))

    standee_rgba.alpha_composite(shadow_img)
    standee_rgba.alpha_composite(scaled_char, (paste_x, paste_y))
    standee_rgb = standee_rgba.convert("RGB")

    standee_rgb.save(f"{BRANDING_DIR}/char_crane.png")
    standee_rgb.save(f"{WEB_HERO_DIR}/char_crane.png")
    standee_rgb.save(f"{DOCS_ART_DIR}/char_crane_candidate_400x840.png")
    print("  ✓ Saved char_crane 400x840 standees")

    # 2. Battle sprite (128x128)
    # Cloud crane's battle stance is the ready-to-shoot pose from poses/crane/telegraph.png
    telegraph_path = f"{PLAYER_DIR}/poses/crane/telegraph.png"
    if os.path.exists(telegraph_path):
        battle_img = Image.open(telegraph_path).convert("RGBA")
    else:
        battle_img = comp.copy()
    battle_dst = f"{PLAYER_DIR}/crane_battle.png"
    battle_img.save(battle_dst)
    print(f"  ✓ Saved {battle_dst}")

    # 3. Idle assets (128x128 & 64x64)
    idle_x3_dst = f"{PLAYER_DIR}/crane_idle_x3.png"
    comp.save(idle_x3_dst)
    party_dst = f"{PARTY_DIR}/crane_idle.png"
    comp.save(party_dst)
    web_idle_dst = f"{WEB_HERO_DIR}/crane_idle.png"
    comp.save(web_idle_dst)
    
    idle_64 = comp.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64_dst = f"{PLAYER_DIR}/crane_idle.png"
    idle_64.save(idle_64_dst)
    print("  ✓ Saved crane idle assets (idle, idle_x3, party/idle, web/idle)")

    # 4. Walk frames (4 frames: 0..3)
    # Build clean walk gait from paperdoll slices
    # Decompose into torso, left leg, right leg
    chassis = Image.open(f"{crane_pd}/chassis/paint_crane_porcelain.png").convert("RGBA")
    w, h = 128, 128
    ch_px = chassis.load()
    assert ch_px is not None

    leg_l = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    leg_r = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    torso = comp.copy()
    t_px = torso.load()
    assert t_px is not None

    for y in range(h):
        for x in range(w):
            p = cast(tuple[int, int, int, int], ch_px[x, y])
            if p[3] > 0 and y >= 92:
                if x <= 62:
                    leg_l.putpixel((x, y), p)
                else:
                    leg_r.putpixel((x, y), p)
                t_px[x, y] = (0, 0, 0, 0) # Clear legs from torso

    walk_frames_128 = []
    # Gait: 4 frames
    gait_offsets = [
        # Frame 0: Left forward (+2px), Right back (-2px), Torso dy=0
        {"torso_dy": 0, "ll_dy": 0, "ll_dx": -2, "lr_dy": 0, "lr_dx": 2},
        # Frame 1: Passing (bob up -2px, Right lifting -4px)
        {"torso_dy": -2, "ll_dy": -2, "ll_dx": 0, "lr_dy": -4, "lr_dx": -1},
        # Frame 2: Right forward (+2px), Left back (-2px), Torso dy=0
        {"torso_dy": 0, "ll_dy": 0, "ll_dx": 2, "lr_dy": 0, "lr_dx": -2},
        # Frame 3: Passing (bob up -2px, Left lifting -4px)
        {"torso_dy": -2, "ll_dy": -4, "ll_dx": -1, "lr_dy": -2, "lr_dx": 0},
    ]

    for i, g in enumerate(gait_offsets):
        f128 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        # paste leg_l
        f128.paste(leg_l, (g["ll_dx"], g["ll_dy"]), leg_l)
        # paste leg_r
        f128.paste(leg_r, (g["lr_dx"], g["lr_dy"]), leg_r)
        # paste torso
        f128.paste(torso, (0, g["torso_dy"]), torso)
        walk_frames_128.append(f128)

        # Save 128x128 and 64x64
        f128.save(f"{PLAYER_DIR}/crane_walk_{i}_x3.png")
        f64 = f128.resize((64, 64), Image.Resampling.LANCZOS)
        f64.save(f"{PLAYER_DIR}/crane_walk_{i}.png")

    # Walk cycle proof
    strip = Image.new("RGBA", (128 * 4, 128), (0, 0, 0, 0))
    for i, fr in enumerate(walk_frames_128):
        strip.alpha_composite(fr, (i * 128, 0))
    strip.save(f"{PLAYER_DIR}/proof_crane_walk_cycle.png")
    print("  ✓ Saved crane walk cycle (0..3, x3, and proof strip)")

    # 5. Portraits:
    # Dialogue bust: 384x480 (from high-res cutout)
    # Head & upper body crop: X=560..870, Y=85..500
    bust_crop = cutout_all.crop((560, 85, 870, 500))
    # Scale bust height to ~420px
    b_scale = 420.0 / bust_crop.height
    bw = int(round(bust_crop.width * b_scale))
    bh = int(round(bust_crop.height * b_scale))
    scaled_bust = bust_crop.resize((bw, bh), Image.Resampling.LANCZOS)
    dialogue_bust = Image.new("RGBA", (384, 480), (0, 0, 0, 0))
    paste_bx = (384 - bw) // 2
    paste_by = 480 - bh
    dialogue_bust.alpha_composite(scaled_bust, (paste_bx, paste_by))
    dialogue_bust.save(f"{PORTRAITS_DIR}/cloud_crane.png")

    # HUD portrait: 128x128 tight head crop
    # Head in 128x128 comp is around (36, 10, 88, 58)
    hud_crop = comp.crop((34, 8, 90, 64))
    h_scale = 100.0 / max(hud_crop.width, hud_crop.height)
    hw = int(round(hud_crop.width * h_scale))
    hh = int(round(hud_crop.height * h_scale))
    scaled_hud = hud_crop.resize((hw, hh), Image.Resampling.LANCZOS)
    hud_p = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hud_p.alpha_composite(scaled_hud, ((128 - hw) // 2, (128 - hh) // 2))
    hud_p.save(f"{PORTRAITS_DIR}/crane.png")
    print("  ✓ Saved crane portraits (crane.png 128x128, cloud_crane.png 384x480)")


def build_bear():
    print("\n=== BUILDING THE IRON BEAR (玄軸熊) OFFICIAL ASSETS ===")
    bear_pd = f"{PLAYER_DIR}/paperdoll/bear"
    comp_path = f"{bear_pd}/proof_paperdoll_bear_composite.png"
    assert os.path.exists(comp_path), f"Missing {comp_path}"
    comp = Image.open(comp_path).convert("RGBA")

    # 1. Standee & Candidate (400x840)
    # Source high-res concept: /tmp/iron_bear_full.png (1024x1024)
    bear_full = Image.open("/tmp/iron_bear_full.png").convert("RGB")
    concept_dst = f"{DOCS_ART_DIR}/iron_bear_concept.png"
    bear_full.save(concept_dst)
    print(f"  ✓ Saved {concept_dst}")

    # Transparent background extraction for bear
    corner = cast(tuple[int, int, int], bear_full.getpixel((0, 0)))
    w, h = bear_full.size
    rgba_bear = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bf_px = bear_full.load()
    rb_px = rgba_bear.load()
    assert bf_px is not None and rb_px is not None

    for y in range(h):
        for x in range(w):
            c = cast(tuple[int, int, int], bf_px[x, y])
            diff = max(abs(c[0] - corner[0]), abs(c[1] - corner[1]), abs(c[2] - corner[2]))
            if diff < 16:
                continue
            elif diff < 28:
                a = int(255 * (diff - 16) / 12.0)
                rb_px[x, y] = (c[0], c[1], c[2], a)
            else:
                rb_px[x, y] = (c[0], c[1], c[2], 255)

    # Bear box: (112, 102, 975, 973)
    char_crop = rgba_bear.crop((110, 100, 978, 975))
    scale = 368.0 / char_crop.width
    sw = int(round(char_crop.width * scale))
    sh = int(round(char_crop.height * scale))
    scaled_char = char_crop.resize((sw, sh), Image.Resampling.LANCZOS)

    standee_rgba = Image.new("RGBA", (400, 840), BG_STUDIO + (255,))
    paste_x = (400 - sw) // 2
    target_ground_y = 785
    paste_y = target_ground_y - sh

    shadow_img = Image.new("RGBA", (400, 840), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_img)
    s_draw.ellipse((200 - 100, target_ground_y - 14, 200 + 100, target_ground_y + 14), fill=(31, 26, 58, 85))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=7))

    standee_rgba.alpha_composite(shadow_img)
    standee_rgba.alpha_composite(scaled_char, (paste_x, paste_y))
    standee_rgb = standee_rgba.convert("RGB")

    standee_rgb.save(f"{BRANDING_DIR}/char_bear.png")
    standee_rgb.save(f"{WEB_HERO_DIR}/char_bear.png")
    standee_rgb.save(f"{DOCS_ART_DIR}/char_bear_candidate_400x840.png")
    print("  ✓ Saved char_bear 400x840 standees")

    # 2. Battle sprite (128x128)
    telegraph_path = f"{PLAYER_DIR}/poses/bear/telegraph.png"
    if os.path.exists(telegraph_path):
        battle_img = Image.open(telegraph_path).convert("RGBA")
    else:
        battle_img = comp.copy()
    battle_dst = f"{PLAYER_DIR}/bear_battle.png"
    battle_img.save(battle_dst)
    print(f"  ✓ Saved {battle_dst}")

    # 3. Idle assets (128x128 & 64x64)
    idle_x3_dst = f"{PLAYER_DIR}/bear_idle_x3.png"
    comp.save(idle_x3_dst)
    party_dst = f"{PARTY_DIR}/bear_idle.png"
    comp.save(party_dst)
    web_idle_dst = f"{WEB_HERO_DIR}/bear_idle.png"
    comp.save(web_idle_dst)
    
    idle_64 = comp.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64_dst = f"{PLAYER_DIR}/bear_idle.png"
    idle_64.save(idle_64_dst)
    print("  ✓ Saved bear idle assets (idle, idle_x3, party/idle, web/idle)")

    # 4. Walk frames (4 frames: 0..3)
    chassis = Image.open(f"{bear_pd}/chassis/paint_bear_amber.png").convert("RGBA")
    w, h = 128, 128
    ch_px = chassis.load()
    assert ch_px is not None

    leg_l = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    leg_r = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    torso = comp.copy()
    t_px = torso.load()
    assert t_px is not None

    for y in range(h):
        for x in range(w):
            p = cast(tuple[int, int, int, int], ch_px[x, y])
            if p[3] > 0 and y >= 88:
                if x <= 63:
                    leg_l.putpixel((x, y), p)
                else:
                    leg_r.putpixel((x, y), p)
                t_px[x, y] = (0, 0, 0, 0)

    walk_frames_128 = []
    gait_offsets = [
        {"torso_dy": 0, "ll_dy": 0, "ll_dx": -2, "lr_dy": 0, "lr_dx": 2},
        {"torso_dy": -2, "ll_dy": -2, "ll_dx": 0, "lr_dy": -4, "lr_dx": -1},
        {"torso_dy": 0, "ll_dy": 0, "ll_dx": 2, "lr_dy": 0, "lr_dx": -2},
        {"torso_dy": -2, "ll_dy": -4, "ll_dx": -1, "lr_dy": -2, "lr_dx": 0},
    ]

    for i, g in enumerate(gait_offsets):
        f128 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        f128.paste(leg_l, (g["ll_dx"], g["ll_dy"]), leg_l)
        f128.paste(leg_r, (g["lr_dx"], g["lr_dy"]), leg_r)
        f128.paste(torso, (0, g["torso_dy"]), torso)
        walk_frames_128.append(f128)

        f128.save(f"{PLAYER_DIR}/bear_walk_{i}_x3.png")
        f64 = f128.resize((64, 64), Image.Resampling.LANCZOS)
        f64.save(f"{PLAYER_DIR}/bear_walk_{i}.png")

    strip = Image.new("RGBA", (128 * 4, 128), (0, 0, 0, 0))
    for i, fr in enumerate(walk_frames_128):
        strip.alpha_composite(fr, (i * 128, 0))
    strip.save(f"{PLAYER_DIR}/proof_bear_walk_cycle.png")
    print("  ✓ Saved bear walk cycle (0..3, x3, and proof strip)")

    # 5. Portraits:
    # Dialogue bust: 384x480 (from high-res cutout)
    # Head & upper body crop: X=200..880, Y=100..700
    bust_crop = rgba_bear.crop((200, 100, 880, 700))
    b_scale = 425.0 / bust_crop.height
    bw = int(round(bust_crop.width * b_scale))
    bh = int(round(bust_crop.height * b_scale))
    scaled_bust = bust_crop.resize((bw, bh), Image.Resampling.LANCZOS)
    dialogue_bust = Image.new("RGBA", (384, 480), (0, 0, 0, 0))
    paste_bx = (384 - bw) // 2
    paste_by = 480 - bh
    dialogue_bust.alpha_composite(scaled_bust, (paste_bx, paste_by))
    dialogue_bust.save(f"{PORTRAITS_DIR}/iron_bear.png")

    # HUD portrait: 128x128 tight head crop
    # Head in 128x128 comp is around (32, 14, 96, 68)
    hud_crop = comp.crop((30, 12, 98, 70))
    h_scale = 100.0 / max(hud_crop.width, hud_crop.height)
    hw = int(round(hud_crop.width * h_scale))
    hh = int(round(hud_crop.height * h_scale))
    scaled_hud = hud_crop.resize((hw, hh), Image.Resampling.LANCZOS)
    hud_p = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hud_p.alpha_composite(scaled_hud, ((128 - hw) // 2, (128 - hh) // 2))
    hud_p.save(f"{PORTRAITS_DIR}/bear.png")
    print("  ✓ Saved bear portraits (bear.png 128x128, iron_bear.png 384x480)")

if __name__ == "__main__":
    build_crane()
    build_bear()
    print("\n✓ ALL OFFICIAL ASSETS BUILT FOR CLOUD CRANE & IRON BEAR!")
