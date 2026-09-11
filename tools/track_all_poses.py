import os
from PIL import Image
import numpy as np

frame_dir = "/opt/side/bravesoul-game/proofs/macaque_frames"
files = sorted([f for f in os.listdir(frame_dir) if f.endswith(".png")])

poses = ["idle", "attack", "skill", "hit", "telegraph", "recover"]
p_imgs = {p: np.array(Image.open(f"/tmp/pose_200_{p}.png").convert("RGBA")) for p in poses}

for idx, f in enumerate(files):
    im = Image.open(os.path.join(frame_dir, f)).convert("RGBA")
    # player area around x: 150..550, y: 200..600
    crop = im.crop((150, 200, 550, 600))
    arr = np.array(crop)
    
    # Let's test attack vs idle vs recover vs hit
    best_p = "unknown"
    best_d = 1e9
    for p in ["idle", "attack", "recover", "hit"]:
        arr_p = p_imgs[p]
        mask = arr_p[:, :, 3] > 100
        # search small window around expected player location
        for y in [30, 45, 60, 75]:
            for x in [20, 60, 100, 140, 180, 220]:
                if y + 200 <= arr.shape[0] and x + 200 <= arr.shape[1]:
                    sub = arr[y:y+200, x:x+200]
                    diff = np.mean(np.abs(sub[mask, :3].astype(int) - arr_p[mask, :3].astype(int)))
                    if diff < best_d:
                        best_d = diff
                        best_p = p
    if idx % 5 == 0 or best_p != "idle":
        print(f"Frame {idx+1:3d} ({f}): pose={best_p} (diff={best_d:.2f})")
