#!/usr/bin/env python3
"""
generate_crane_proof_sheet.py
Creates a composite 3x2 preview sheet with labels of the 6 Cloud Crane combat action poses
for visual inspection, vision analysis, and proof verification.
"""

import os
from PIL import Image, ImageDraw

REPO_ROOT = "/opt/side/bravesoul-game"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/crane"
PROOF_PATH = f"{REPO_ROOT}/game/assets/sprites/player/proof_crane_combat_poses_640.png"
PROOF_MAGENTA = f"{REPO_ROOT}/game/assets/sprites/player/proof_crane_combat_poses_magenta.png"

order = ["idle", "telegraph", "attack", "skill", "hit", "recover"]
titles = [
    "1. IDLE (白鶴獨立)",
    "2. TELEGRAPH (蓄力拉弦)",
    "3. ATTACK (風弦疾射)",
    "4. SKILL (天元風暴)",
    "5. HIT (受挫架隔)",
    "6. RECOVER (滑步收勢)"
]

# Sheet size: 3 columns x 2 rows, each tile 160x170 (128x128 sprite + title banner)
cols, rows = 3, 2
tile_w, tile_h = 160, 170
sheet = Image.new("RGBA", (cols * tile_w + 20, rows * tile_h + 30), (28, 24, 40, 255))
s_draw = ImageDraw.Draw(sheet)

# Magenta backdrop test sheet
mag_sheet = Image.new("RGBA", (cols * tile_w + 20, rows * tile_h + 30), (255, 0, 255, 255))
m_draw = ImageDraw.Draw(mag_sheet)

for i, p in enumerate(order):
    col = i % 3
    row = i // 3
    x = 10 + col * tile_w
    y = 15 + row * tile_h
    
    # Background card
    s_draw.rounded_rectangle([x, y, x + tile_w - 10, y + tile_h - 10], radius=8, fill=(42, 36, 56, 255), outline=(90, 75, 110, 255))
    m_draw.rounded_rectangle([x, y, x + tile_w - 10, y + tile_h - 10], radius=8, fill=(42, 36, 56, 255), outline=(90, 75, 110, 255))
    
    # Title
    s_draw.text((x + 12, y + 8), titles[i], fill=(255, 215, 64, 255))
    m_draw.text((x + 12, y + 8), titles[i], fill=(255, 215, 64, 255))
    
    # Sprite
    p_img = Image.open(f"{POSES_DIR}/{p}.png").convert("RGBA")
    spr_x = x + (tile_w - 10 - 128) // 2
    spr_y = y + 26
    sheet.alpha_composite(p_img, (spr_x, spr_y))
    mag_sheet.alpha_composite(p_img, (spr_x, spr_y))

sheet.save(PROOF_PATH)
mag_sheet.save(PROOF_MAGENTA)
print(f"✓ Saved proof sheet: {PROOF_PATH}")
print(f"✓ Saved magenta proof sheet: {PROOF_MAGENTA}")

# Generate zoomed inspection crops for vision verification
idle_img = Image.open(f"{POSES_DIR}/idle.png").convert("RGBA")
tele_img = Image.open(f"{POSES_DIR}/telegraph.png").convert("RGBA")
atk_img = Image.open(f"{POSES_DIR}/attack.png").convert("RGBA")
skill_img = Image.open(f"{POSES_DIR}/skill.png").convert("RGBA")

# 1. Head & Crest crop (40, 10, 85, 58) 3x zoom
crop_head = idle_img.crop((40, 10, 86, 58)).resize((138 * 3, 144 * 3), Image.Resampling.NEAREST)
crop_head.save("/tmp/crane_verify_head.png")

# 2. Weapon Bow crop (78, 50, 108, 100) 3x zoom
crop_bow = idle_img.crop((78, 50, 108, 100)).resize((90 * 3, 150 * 3), Image.Resampling.NEAREST)
crop_bow.save("/tmp/crane_verify_weapon.png")

# 3. Key crop (30, 30, 50, 56) 4x zoom
crop_key = idle_img.crop((30, 30, 50, 56)).resize((80 * 4, 104 * 4), Image.Resampling.NEAREST)
crop_key.save("/tmp/crane_verify_key.png")

# 4. Telegraph drawn bow & arrow (60, 40, 124, 90) 3x zoom
crop_tele = tele_img.crop((60, 40, 124, 90)).resize((192 * 2, 150 * 2), Image.Resampling.NEAREST)
crop_tele.save("/tmp/crane_verify_telegraph_arrow.png")

# 5. Skill tempest wings (10, 10, 120, 100) 2x zoom
crop_skill = skill_img.crop((10, 10, 120, 100)).resize((220 * 2, 180 * 2), Image.Resampling.NEAREST)
crop_skill.save("/tmp/crane_verify_skill_tempest.png")

print("✓ Saved 5 zoomed verification crops to /tmp/")
