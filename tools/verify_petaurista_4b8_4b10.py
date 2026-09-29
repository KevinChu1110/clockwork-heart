#!/usr/bin/env python3
import os
import sys

sys.path = [p for p in sys.path if not p.startswith('/tmp')]

from PIL import Image, ImageChops
import numpy as np

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/petaurista"
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
        # body zone y < 118
        body_diff = int(np.sum(np.any(arr[:118, :, :] > 0, axis=-1)))
        print(f"  {p1:10s} vs {p2:10s} : body diff={body_diff:5d} px")
        assert body_diff >= 4000, f"FAIL: {p1} vs {p2} diff too low ({body_diff} < 4000)!"

print("✓ Rule 4b-10 PASSED: All pairs have high mechanical articulation (>= 4000 px)!")

print("\n=== Rule 4b-8: Comparison with existing assets ===")
party_idle = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/party/petaurista_idle.png").convert("RGBA")
for p in ['telegraph', 'attack', 'recover', 'skill', 'hit']:
    diff = ImageChops.difference(imgs[p], party_idle)
    arr = np.array(diff)
    body_diff = int(np.sum(np.any(arr[:118, :, :] > 0, axis=-1)))
    print(f"  {p:10s} vs party_idle : body diff={body_diff:5d} px")
    assert body_diff >= 4000, f"FAIL: {p} is too close to existing party_idle! ({body_diff})"

print("✓ Rule 4b-8 PASSED: No action pose is a copy of existing party/battle assets!")
