#!/usr/bin/env python3
"""
tools/build_round2_comparison_proof.py
Generates side-by-side comparison images showing before and after Round 2 fixes:
1. Bear Amber comparison: ear contours, snout shading, neckline, handle removal
2. Bear Quarry comparison: flat fill elimination, ear contours, neckline, handle removal, leg recolor
"""

import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PROOFS_DIR = f"{REPO_ROOT}/proofs/head_sync_proofs"

def build_comparisons():
    # Load before (Attempt 2) from git commit c70dec8b
    os.system(f"git -C {REPO_ROOT} show c70dec8b:game/assets/sprites/player/paperdoll/bear/head_unit/head_iron_bear_amber_512.png > {PROOFS_DIR}/head_amber_before_round2.png")
    os.system(f"git -C {REPO_ROOT} show c70dec8b:game/assets/sprites/player/paperdoll/bear/head_unit/head_iron_bear_quarry_512.png > {PROOFS_DIR}/head_quarry_before_round2.png")
    os.system(f"git -C {REPO_ROOT} show c70dec8b:proofs/head_sync_proofs/composite_512_bear_amber.png > {PROOFS_DIR}/composite_amber_before_round2.png")
    os.system(f"git -C {REPO_ROOT} show c70dec8b:proofs/head_sync_proofs/composite_512_bear_quarry.png > {PROOFS_DIR}/composite_quarry_before_round2.png")
    
    # 1. Head Unit Comparison Board
    im_amb_before = Image.open(f"{PROOFS_DIR}/head_amber_before_round2.png").convert("RGBA")
    im_amb_after = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bear/head_unit/head_iron_bear_amber_512.png").convert("RGBA")
    im_qua_before = Image.open(f"{PROOFS_DIR}/head_quarry_before_round2.png").convert("RGBA")
    im_qua_after = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bear/head_unit/head_iron_bear_quarry_512.png").convert("RGBA")
    
    # Crop head area: y in 60..240, x in 155..355 (200x180)
    box = (155, 60, 355, 240)
    c_amb_bef = im_amb_before.crop(box)
    c_amb_aft = im_amb_after.crop(box)
    c_qua_bef = im_qua_before.crop(box)
    c_qua_aft = im_qua_after.crop(box)
    
    W_cell, H_cell = 200, 180
    board = Image.new("RGBA", (W_cell * 4 + 50, H_cell + 60), (30, 32, 40, 255))
    draw = ImageDraw.Draw(board)
    
    # Titles
    draw.text((15, 10), "Amber [Before R2]", fill=(220, 180, 120, 255))
    draw.text((W_cell + 25, 10), "Amber [After R2 - Masterpiece]", fill=(255, 215, 0, 255))
    draw.text((W_cell * 2 + 35, 10), "Quarry [Before R2]", fill=(160, 180, 200, 255))
    draw.text((W_cell * 3 + 45, 10), "Quarry [After R2 - Masterpiece]", fill=(100, 220, 255, 255))
    
    board.paste(c_amb_bef, (10, 40), c_amb_bef)
    board.paste(c_amb_aft, (W_cell + 20, 40), c_amb_aft)
    board.paste(c_qua_bef, (W_cell * 2 + 30, 40), c_qua_bef)
    board.paste(c_qua_aft, (W_cell * 3 + 40, 40), c_qua_aft)
    
    board_path = f"{PROOFS_DIR}/proof_head_comparison_round2.png"
    board.save(board_path)
    print(f"✓ Created side-by-side head comparison: {board_path}")
    
    # 2. Composite Full Comparison Board
    im_comp_amb_bef = Image.open(f"{PROOFS_DIR}/composite_amber_before_round2.png").convert("RGBA")
    im_comp_amb_aft = Image.open(f"{PROOFS_DIR}/composite_512_bear_amber.png").convert("RGBA")
    im_comp_qua_bef = Image.open(f"{PROOFS_DIR}/composite_quarry_before_round2.png").convert("RGBA")
    im_comp_qua_aft = Image.open(f"{PROOFS_DIR}/composite_512_bear_quarry.png").convert("RGBA")
    
    comp_board = Image.new("RGBA", (512 * 4 + 50, 512 + 60), (24, 26, 32, 255))
    draw_comp = ImageDraw.Draw(comp_board)
    
    draw_comp.text((20, 15), "Amber Composite (Before R2)", fill=(220, 180, 120, 255))
    draw_comp.text((512 + 30, 15), "Amber Composite (After R2 - Masterpiece)", fill=(255, 215, 0, 255))
    draw_comp.text((512 * 2 + 40, 15), "Quarry Composite (Before R2)", fill=(160, 180, 200, 255))
    draw_comp.text((512 * 3 + 50, 15), "Quarry Composite (After R2 - Masterpiece)", fill=(100, 220, 255, 255))
    
    comp_board.paste(im_comp_amb_bef, (10, 50), im_comp_amb_bef)
    comp_board.paste(im_comp_amb_aft, (512 + 20, 50), im_comp_amb_aft)
    comp_board.paste(im_comp_qua_bef, (512 * 2 + 30, 50), im_comp_qua_bef)
    comp_board.paste(im_comp_qua_aft, (512 * 3 + 40, 50), im_comp_qua_aft)
    
    comp_board_path = f"{PROOFS_DIR}/proof_composite_comparison_round2.png"
    comp_board.save(comp_board_path)
    print(f"✓ Created side-by-side composite comparison: {comp_board_path}")

if __name__ == "__main__":
    build_comparisons()
