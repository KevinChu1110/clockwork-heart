#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PROOFS_DIR = f"{REPO_ROOT}/proofs/head_sync_proofs"

# Extract true Before from c70dec8b
os.system(f"git -C {REPO_ROOT} show c70dec8b:proofs/head_sync_proofs/composite_512_bear_amber.png > {PROOFS_DIR}/composite_amber_before_round2.png")
os.system(f"git -C {REPO_ROOT} show c70dec8b:proofs/head_sync_proofs/composite_512_bear_quarry.png > {PROOFS_DIR}/composite_quarry_before_round2.png")

im_a_bef = Image.open(f"{PROOFS_DIR}/composite_amber_before_round2.png").convert("RGBA")
im_a_aft = Image.open(f"{PROOFS_DIR}/composite_512_bear_amber.png").convert("RGBA")

im_q_bef = Image.open(f"{PROOFS_DIR}/composite_quarry_before_round2.png").convert("RGBA")
im_q_aft = Image.open(f"{PROOFS_DIR}/composite_512_bear_quarry.png").convert("RGBA")

arr_a_bef = np.array(im_a_bef).astype(int)
arr_a_aft = np.array(im_a_aft).astype(int)

arr_q_bef = np.array(im_q_bef).astype(int)
arr_q_aft = np.array(im_q_aft).astype(int)

diff_a = np.max(np.abs(arr_a_aft - arr_a_bef), axis=2)
diff_q = np.max(np.abs(arr_q_aft - arr_q_bef), axis=2)

mask_a = diff_a > 10
mask_q = diff_q > 10

print("=== Amber Before vs After Pixel Diff ===")
print(f"Total diff > 10 pixels: {np.sum(mask_a)}")
if np.sum(mask_a) > 0:
    ya, xa = np.where(mask_a)
    print(f"Amber diff bbox: x in {xa.min()}..{xa.max()}, y in {ya.min()}..{ya.max()}")
    
    # Check head region (y < 220):
    head_diff = np.sum(mask_a[:220, :])
    print(f"Amber head region diff: {head_diff} (Round 2 head refinement)")
    
    # Check rod region (x in 280..400, y in 280..500):
    rod_diff = np.sum(mask_a[280:505, 280:400])
    print(f"Amber rod region diff: {rod_diff}")

print("\n=== Quarry Before vs After Pixel Diff ===")
print(f"Total diff > 10 pixels: {np.sum(mask_q)}")
if np.sum(mask_q) > 0:
    yq, xq = np.where(mask_q)
    print(f"Quarry diff bbox: x in {xq.min()}..{xq.max()}, y in {yq.min()}..{yq.max()}")
    
    # Check head region (y < 220):
    head_diff_q = np.sum(mask_q[:220, :])
    print(f"Quarry head region diff: {head_diff_q} (Round 2 head refinement)")
    
    # Check rod and leg region (x in 280..400, y in 280..505):
    rod_leg_diff = np.sum(mask_q[280:505, 280:400])
    print(f"Quarry rod + leg region diff: {rod_leg_diff}")
