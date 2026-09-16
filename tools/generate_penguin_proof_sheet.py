#!/usr/bin/env python3
"""
generate_penguin_proof_sheet.py
Creates composite 3x2 preview sheets with labels of the 6 Steam Penguin combat action poses
for visual inspection, vision analysis, and proof verification.
"""

import os
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/penguin"
PROOF_PATH = f"{REPO_ROOT}/game/assets/sprites/player/proof_penguin_combat_poses_640.png"
PROOF_MAGENTA = f"{REPO_ROOT}/game/assets/sprites/player/proof_penguin_combat_poses_magenta.png"

font = ImageFont.truetype("/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf", 13)

order = ["idle", "telegraph", "attack", "skill", "hit", "recover"]
titles = [
    "1. IDLE (蒸汽戒備)",
    "2. TELEGRAPH (過壓蓄勢)",
    "3. ATTACK (雙管轟擊)",
    "4. SKILL (天穹連射)",
    "5. HIT (受挫洩壓)",
    "6. RECOVER (錨定收勢)"
]

cols, rows = 3, 2
tile_w, tile_h = 160, 170

# Sheet 1: Dark theme presentation card sheet
sheet = Image.new("RGBA", (cols * tile_w + 20, rows * tile_h + 30), (28, 24, 40, 255))
s_draw = ImageDraw.Draw(sheet)

# Sheet 2: Pure Magenta verification backdrop sheet (sprites placed directly on magenta)
mag_sheet = Image.new("RGBA", (cols * tile_w + 20, rows * tile_h + 30), (255, 0, 255, 255))
m_draw = ImageDraw.Draw(mag_sheet)

for i, p in enumerate(order):
    col = i % 3
    row = i // 3
    x = 10 + col * tile_w
    y = 15 + row * tile_h
    
    # Background card on dark sheet
    s_draw.rounded_rectangle([x, y, x + tile_w - 10, y + tile_h - 10], radius=8, fill=(42, 36, 56, 255), outline=(90, 75, 110, 255))
    
    # Background card on magenta sheet
    m_draw.rounded_rectangle([x, y, x + tile_w - 10, y + tile_h - 10], radius=8, fill=(42, 36, 56, 255), outline=(90, 75, 110, 255))
    
    # Titles
    s_draw.text((x + 12, y + 8), titles[i], font=font, fill=(255, 215, 64, 255))
    m_draw.text((x + 12, y + 8), titles[i], font=font, fill=(255, 215, 64, 255))
    
    # Sprite
    p_img = Image.open(f"{POSES_DIR}/{p}.png").convert("RGBA")
    spr_x = x + (tile_w - 10 - 128) // 2
    spr_y = y + 26
    sheet.alpha_composite(p_img, (spr_x, spr_y))
    # Place directly on magenta
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

# 1. Head dome & Goggles crop (30, 15, 88, 58) 3x zoom
crop_head = idle_img.crop((30, 15, 88, 58)).resize(((88 - 30) * 3, (58 - 15) * 3), Image.Resampling.NEAREST)
crop_head.save("/tmp/penguin_verify_head.png")

# 2. Weapon Harpoon Gun crop (70, 45, 120, 90) 3x zoom
crop_gun = idle_img.crop((70, 45, 120, 90)).resize(((120 - 70) * 3, (90 - 45) * 3), Image.Resampling.NEAREST)
crop_gun.save("/tmp/penguin_verify_weapon.png")

# 3. Key & Boiler crop (5, 10, 40, 75) 3x zoom
crop_key = idle_img.crop((5, 10, 40, 75)).resize(((40 - 5) * 3, (75 - 10) * 3), Image.Resampling.NEAREST)
crop_key.save("/tmp/penguin_verify_key_boiler.png")

# 4. Attack blast crop (80, 45, 126, 85) 3x zoom
crop_atk = atk_img.crop((80, 45, 126, 85)).resize(((126 - 80) * 3, (85 - 45) * 3), Image.Resampling.NEAREST)
crop_atk.save("/tmp/penguin_verify_attack_blast.png")

# 5. Skill skyward salvo crop (70, 10, 120, 70) 2x zoom
crop_skill = skill_img.crop((70, 10, 120, 70)).resize(((120 - 70) * 2, (70 - 10) * 2), Image.Resampling.NEAREST)
crop_skill.save("/tmp/penguin_verify_skill_salvo.png")

print("✓ Saved 5 zoomed verification crops to /tmp/")
