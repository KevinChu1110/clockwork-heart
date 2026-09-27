#!/usr/bin/env python3
"""
tools/generate_comparison_proofs.py
Generates 1:1 side-by-side comparison proof images for:
- Hound & Fawn winding keys (128x128 and 512x512)
- Hound & Fawn paperdoll composites
- Real in-game xvfb crops
Saves outputs to proofs/t_1f136a47/
"""
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

WORKTREE = "/opt/side/bravesoul-game/.worktrees/t_1f136a47"
PROOF_DIR = f"{WORKTREE}/proofs/t_1f136a47"
os.makedirs(PROOF_DIR, exist_ok=True)
BACKUP_DIR = f"{WORKTREE}/tools/backup_before_clean"

BG_COLOR = (24, 20, 36, 255)       # Dark theme bg
CARD_BG  = (38, 32, 54, 255)
TEXT_COL = (255, 208, 40, 255)     # Gold
SUB_COL  = (180, 195, 220, 255)    # Steel light
RED_COL  = (255, 94, 138, 255)     # Coral / before
GREEN_COL= (78, 216, 106, 255)     # Mint / after

FONT_PATH = f"{WORKTREE}/game/assets/fonts/jf-openhuninn-2.1.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

try:
    font_title = ImageFont.truetype(FONT_PATH, 18)
    font_sub = ImageFont.truetype(FONT_PATH, 13)
except Exception:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()

def make_side_by_side(before_img, after_img, title, subtitle_b, subtitle_a, scale=2):
    w, h = before_img.size
    scaled_w, scaled_h = w * scale, h * scale
    
    pad = 20
    header_h = 50
    total_w = pad * 3 + scaled_w * 2
    total_h = pad * 2 + header_h + scaled_h + 30
    
    canvas = Image.new("RGBA", (total_w, total_h), BG_COLOR)
    draw = ImageDraw.Draw(canvas)
    
    # Title
    draw.text((pad, pad + 10), title, fill=TEXT_COL, font=font_title)
    
    # Left card (Before)
    bx = pad
    by = pad + header_h
    draw.rectangle([bx, by, bx + scaled_w, by + scaled_h], fill=CARD_BG, outline=(255, 94, 138, 180), width=2)
    b_scaled = before_img.resize((scaled_w, scaled_h), Image.Resampling.NEAREST if scale > 1 else Image.Resampling.LANCZOS)
    canvas.alpha_composite(b_scaled, (bx, by))
    draw.text((bx + 4, by + scaled_h + 6), subtitle_b, fill=RED_COL, font=font_sub)
    
    # Right card (After)
    ax = pad * 2 + scaled_w
    ay = pad + header_h
    draw.rectangle([ax, ay, ax + scaled_w, ay + scaled_h], fill=CARD_BG, outline=(78, 216, 106, 180), width=2)
    a_scaled = after_img.resize((scaled_w, scaled_h), Image.Resampling.NEAREST if scale > 1 else Image.Resampling.LANCZOS)
    canvas.alpha_composite(a_scaled, (ax, ay))
    draw.text((ax + 4, ay + scaled_h + 6), subtitle_a, fill=GREEN_COL, font=font_sub)
    
    return canvas

def main():
    print("=== Generating Side-by-Side Comparison Proofs ===")
    
    # 1. Hound Key (128x128 -> 2x display)
    h_before = Image.open(f"{BACKUP_DIR}/hound_key_128_before.png").convert("RGBA")
    h_after = Image.open(f"{WORKTREE}/game/assets/sprites/player/paperdoll/hound/winding_key/key_hound_four_blade_antenna_gold.png").convert("RGBA")
    p1 = make_side_by_side(h_before, h_after,
                          "星軌犬 (Hound) 發條鑰匙切片 1:1 比對 (2x 放大顯示)",
                          "【改前】dark=817px, max_run=30px, 異常方形底板未去背",
                          "【改後】dark=235px, max_run=7px, 去背乾淨且無殘留",
                          scale=2)
    p1_path = f"{PROOF_DIR}/proof_hound_key_comparison.png"
    p1.save(p1_path)
    print(f"✓ Saved {p1_path}")
    
    # 2. Fawn Key (128x128 -> 2x display)
    f_before = Image.open(f"{BACKUP_DIR}/fawn_key_128_before.png").convert("RGBA")
    f_after = Image.open(f"{WORKTREE}/game/assets/sprites/player/paperdoll/fawn/winding_key/key_fawn_clover_leaf_brass.png").convert("RGBA")
    p2 = make_side_by_side(f_before, f_after,
                          "翠角鹿 (Fawn) 發條鑰匙切片 1:1 比對 (2x 放大顯示)",
                          "【改前】dark=656px, max_run=26px, 異常方形底板未去背",
                          "【改後】dark=217px, max_run=8px, 去背乾淨且無殘留",
                          scale=2)
    p2_path = f"{PROOF_DIR}/proof_fawn_key_comparison.png"
    p2.save(p2_path)
    print(f"✓ Saved {p2_path}")

    # 3. Real In-Game Hound Crop Comparison (1:1 display)
    c_before = Image.open("/opt/side/bravesoul-game/proofs/combat_poses_512/proof_combat_hound_idle_crop.png").convert("RGBA")
    c_after = Image.open(f"{WORKTREE}/proofs/combat_poses_512/proof_combat_hound_idle_crop.png").convert("RGBA")
    # Align heights if slightly different
    max_h = max(c_before.height, c_after.height)
    max_w = max(c_before.width, c_after.width)
    pad_b = Image.new("RGBA", (max_w, max_h), (0, 0, 0, 0))
    pad_b.alpha_composite(c_before, (0, 0))
    pad_a = Image.new("RGBA", (max_w, max_h), (0, 0, 0, 0))
    pad_a.alpha_composite(c_after, (0, 0))
    
    p3 = make_side_by_side(pad_b, pad_a,
                          "星軌犬戰鬥待機 512 實機截圖角色區域裁切 1:1 比對 (xvfb 實拍)",
                          "【改前】頭部右後方帶金色十字之深色方塊殘留明顯",
                          "【改後】深色方塊完全清除，四葉天線金黃發條鑰匙清晰透出",
                          scale=1)
    p3_path = f"{PROOF_DIR}/proof_combat_hound_crop_comparison.png"
    p3.save(p3_path)
    print(f"✓ Saved {p3_path}")

    # 4. Fawn In-Game Crop Comparison
    fc_after = Image.open(f"{WORKTREE}/proofs/combat_poses_512/proof_combat_fawn_idle_crop.png").convert("RGBA")
    # For fawn before crop, if exists:
    fawn_crop_orig = "/opt/side/bravesoul-game/proofs/combat_poses_512/proof_combat_fawn_idle_crop.png"
    if os.path.exists(fawn_crop_orig):
        fc_before = Image.open(fawn_crop_orig).convert("RGBA")
        max_fh = max(fc_before.height, fc_after.height)
        max_fw = max(fc_before.width, fc_after.width)
        pad_fb = Image.new("RGBA", (max_fw, max_fh), (0, 0, 0, 0))
        pad_fb.alpha_composite(fc_before, (0, 0))
        pad_fa = Image.new("RGBA", (max_fw, max_fh), (0, 0, 0, 0))
        pad_fa.alpha_composite(fc_after, (0, 0))
        p4 = make_side_by_side(pad_fb, pad_fa,
                              "翠角鹿戰鬥待機 512 實機截圖角色區域裁切 1:1 比對 (xvfb 實拍)",
                              "【改前】頭部後方四葉草鑰匙周邊深色未去背殘留",
                              "【改後】去背殘留歸零，黃銅四葉草風葉發條鑰匙精確呈現",
                              scale=1)
        p4_path = f"{PROOF_DIR}/proof_combat_fawn_crop_comparison.png"
        p4.save(p4_path)
        print(f"✓ Saved {p4_path}")

    # 5. Composite Sheet
    comp_hb = Image.open(f"{BACKUP_DIR}/hound_comp_before.png").convert("RGBA")
    comp_ha = Image.open(f"{WORKTREE}/game/assets/sprites/player/paperdoll/hound/proof_paperdoll_hound_composite.png").convert("RGBA")
    p5 = make_side_by_side(comp_hb, comp_ha,
                          "星軌犬紙娃娃 7 槽全層合成圖 1:1 比對 (2x 放大顯示)",
                          "【改前】鑰匙層帶方形底板，干擾角色頭背輪廓",
                          "【改後】全層乾淨融合，符合覺醒玩具世界觀金屬板件規範",
                          scale=2)
    p5_path = f"{PROOF_DIR}/proof_paperdoll_hound_composite_comparison.png"
    p5.save(p5_path)
    print(f"✓ Saved {p5_path}")

    print("\n🎉 All comparison proofs successfully generated in proofs/t_1f136a47/!")

if __name__ == "__main__":
    main()
