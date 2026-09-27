import os
import numpy as np
from PIL import Image, ImageChops

REPO_ROOT = "/opt/side/bravesoul-game"
comp_path = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/owl/proof_paperdoll_owl_composite.png"
im = Image.open(comp_path).convert("RGBA")
arr = np.array(im)
counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print("Owl baseline shadow counts (118..127):", counts)
bbox = im.getbbox()
print("Owl baseline bbox:", bbox)

poses = ['idle', 'telegraph', 'attack', 'skill', 'hit', 'recover']
base_dir = f"{REPO_ROOT}/game/assets/sprites/player/poses/owl"
images = {}
for p in poses:
    path = f"{base_dir}/{p}.png"
    if os.path.exists(path):
        images[p] = Image.open(path).convert('RGBA')

print("\n--- Current Owl Poses ---")
for p, img in images.items():
    bb = img.getbbox()
    l, t, r, b = bb[0], bb[1], 128 - bb[2], 128 - bb[3]
    ar = np.array(img)
    sc = [int(np.sum(ar[y, :, 3] > 20)) for y in range(118, 128)]
    print(f"{p:10s}: bbox={bb}, L={l}, T={t}, R={r}, B={b}, shadow={sc}")

print("\n--- Diffs vs idle ---")
for p in ['telegraph', 'attack', 'skill', 'hit', 'recover']:
    if p in images:
        diff = ImageChops.difference(images['idle'], images[p])
        ch = int(np.sum(np.any(np.array(diff) > 0, axis=-1)))
        print(f"{p:10s} vs idle: {ch} px ({ch/(128*128)*100:.1f}%)")

print("\n--- Translation search ---")
for p in ['telegraph', 'attack', 'skill', 'hit', 'recover']:
    if p in images:
        min_diff = 999999
        best_shift = None
        for dx in range(-12, 13):
            for dy in range(-12, 13):
                shifted = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
                shifted.paste(images['idle'], (dx, dy), images['idle'])
                d = ImageChops.difference(shifted, images[p])
                cnt = int(np.sum(np.any(np.array(d) > 0, axis=-1)))
                if cnt < min_diff:
                    min_diff = cnt
                    best_shift = (dx, dy)
        print(f"{p:10s}: min_diff={min_diff} at {best_shift}")
