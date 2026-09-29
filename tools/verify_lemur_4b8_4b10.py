#!/usr/bin/env python3
"""
verify_lemur_4b8_4b10.py
Verifies Rule 4b-10 (Pairwise Difference Matrix >= 4000px in body zone y < 118)
and Rule 4b-8 (No copy of existing party/battle assets, with battle==attack per review.md 4b-8-1).
"""
import os
import sys

from PIL import Image, ImageChops
import numpy as np

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/lemur"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
POSES = ['idle', 'telegraph', 'attack', 'recover', 'skill', 'hit']

imgs = {p: Image.open(f"{POSES_DIR}/{p}.png").convert("RGBA") for p in POSES}

print("=== Rule 4b-10: Pairwise Difference Matrix (Body zone y < 118) ===")
matrix = {}
for i, p1 in enumerate(POSES):
    for j, p2 in enumerate(POSES):
        if i >= j:
            continue
        diff = ImageChops.difference(imgs[p1], imgs[p2])
        arr = np.array(diff)
        body_diff = int(np.sum(np.any(arr[:118, :, :] > 0, axis=-1)))
        print(f"  {p1:10s} vs {p2:10s} : body diff={body_diff:5d} px")
        assert body_diff >= 4000, f"FAIL: {p1} vs {p2} diff too low ({body_diff} < 4000)!"

print("✓ Rule 4b-10 PASSED: All pairs have high mechanical articulation (>= 4000 px)!")

print("\n=== Rule 4b-8: Comparison with existing party_idle ===")
party_idle = Image.open(f"{PLAYER_DIR}/party/lemur_idle.png").convert("RGBA")
for p in ['telegraph', 'attack', 'recover', 'skill', 'hit']:
    diff = ImageChops.difference(imgs[p], party_idle)
    arr = np.array(diff)
    body_diff = int(np.sum(np.any(arr[:118, :, :] > 0, axis=-1)))
    print(f"  {p:10s} vs party_idle : body diff={body_diff:5d} px")
    assert body_diff >= 4000, f"FAIL: {p} is too close to existing party_idle! ({body_diff})"

print("✓ Rule 4b-8 PASSED: No action pose is a copy of existing party_idle!")

print("\n=== Battle vs Idle & Battle vs Attack Verification ===")
battle_img = Image.open(f"{PLAYER_DIR}/lemur_battle.png").convert("RGBA")
# Battle vs Idle must have significant difference
diff_bi = ImageChops.difference(battle_img, imgs['idle'])
arr_bi = np.array(diff_bi)
body_diff_bi = int(np.sum(np.any(arr_bi[:118, :, :] > 0, axis=-1)))
print(f"  lemur_battle vs idle   : body diff={body_diff_bi:5d} px")
assert body_diff_bi >= 4000, f"FAIL: lemur_battle vs idle diff too low ({body_diff_bi} < 4000)!"

# Battle vs Attack is identical per review.md 4b-8-1
diff_ba = ImageChops.difference(battle_img, imgs['attack'])
arr_ba = np.array(diff_ba)
diff_ba_count = int(np.sum(np.any(arr_ba > 0, axis=-1)))
print(f"  lemur_battle vs attack : diff={diff_ba_count:5d} px (0 is expected per review.md 4b-8-1)")
assert diff_ba_count == 0, f"FAIL: lemur_battle is not attack ({diff_ba_count})!"

print("✓ Battle vs Idle & Attack PASSED: Significant difference vs idle, identical to attack!")
