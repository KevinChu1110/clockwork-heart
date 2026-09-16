#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PROOFS_DIR = f"{REPO_ROOT}/proofs"
os.makedirs(PROOFS_DIR, exist_ok=True)

def generate_proofs():
    # 1. tiger_battle.png crop torso + hands >= 10x
    battle = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/tiger_battle.png")
    # Torso + both hands: x=5..100, y=40..115
    b_crop = battle.crop((5, 40, 100, 115))
    b_zoom = b_crop.resize((b_crop.width * 10, b_crop.height * 10), Image.Resampling.NEAREST)
    b_path = f"{PROOFS_DIR}/tiger_battle_torso_zoom_10x.png"
    b_zoom.save(b_path)
    print(f"✓ Saved {b_path} (size: {b_zoom.size})")

    # 2. char_tiger.png crop torso + hands
    char = Image.open(f"{REPO_ROOT}/branding/char_tiger.png")
    # Torso + both hands: x=10..390, y=340..720
    c_crop = char.crop((10, 340, 390, 720))
    c_zoom = c_crop.resize((c_crop.width * 2, c_crop.height * 2), Image.Resampling.LANCZOS)
    c_path = f"{PROOFS_DIR}/char_tiger_torso_zoom_10x.png"
    c_zoom.save(c_path)
    print(f"✓ Saved {c_path} (size: {c_zoom.size})")

    # 3. char_tiger.png scaled to 128px width
    w128 = 128
    h128 = int(round(char.height * (128.0 / char.width)))
    char_128 = char.resize((w128, h128), Image.Resampling.LANCZOS)
    c128_path = f"{PROOFS_DIR}/char_tiger_128px.png"
    char_128.save(c128_path)
    print(f"✓ Saved {c128_path} (size: {char_128.size})")

    # 4. Measure char_tiger.png col 399 and row 0 non-bg pixels
    BG_COLOR = (235, 226, 209)
    char_arr = np.array(char)
    diff_bg = np.max(np.abs(char_arr.astype(int) - np.array(BG_COLOR).astype(int)), axis=2)
    col_399_non_bg = int(np.sum(diff_bg[:, 399] > 15))
    row_0_non_bg = int(np.sum(diff_bg[0, :] > 15))
    col_0_non_bg = int(np.sum(diff_bg[:, 0] > 15))
    row_839_non_bg = int(np.sum(diff_bg[839, :] > 15))
    
    char_mask = diff_bg > 15
    ys, xs = np.where(char_mask)
    left_margin = int(xs.min())
    right_margin = int(399 - xs.max())
    top_margin = int(ys.min())
    bottom_margin = int(839 - ys.max())
    
    print("=== MEASUREMENTS FOR SUMMARY ===")
    print(f"char_tiger.png col 399 non-bg pixels: {col_399_non_bg}")
    print(f"char_tiger.png row 0 non-bg pixels: {row_0_non_bg}")
    print(f"char_tiger.png col 0 non-bg pixels: {col_0_non_bg}")
    print(f"char_tiger.png row 839 non-bg pixels: {row_839_non_bg}")
    print(f"Margins: Left={left_margin}px, Right={right_margin}px, Top={top_margin}px, Bottom={bottom_margin}px")

    # 5. Four walk frames side by side proof
    strip = Image.new("RGBA", (128 * 4, 128), (0, 0, 0, 0))
    for i in range(4):
        fr = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/tiger_walk_{i}_x3.png")
        strip.alpha_composite(fr, (i * 128, 0))
    strip_zoom = strip.resize((strip.width * 2, strip.height * 2), Image.Resampling.NEAREST)
    strip_path = f"{PROOFS_DIR}/tiger_walk_cycle_4frames_proof.png"
    strip_zoom.save(strip_path)
    print(f"✓ Saved {strip_path}")

if __name__ == "__main__":
    generate_proofs()
