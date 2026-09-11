import os
import glob
import subprocess
import numpy as np
from PIL import Image

mp4 = "/opt/side/bravesoul-game/proofs/combat_feel/macaque_combat.mp4"
tmp = "/tmp/macaque_all_frames"
os.system(f"rm -rf {tmp} && mkdir -p {tmp}")
subprocess.run(["ffmpeg", "-loglevel", "error", "-i", mp4, f"{tmp}/f_%04d.png"])
frames = sorted(glob.glob(f"{tmp}/f_*.png"))
print(f"Total frames: {len(frames)}")

# Analyze each frame:
# Enemy damage float area: x: 750~1100, y: 80~380
# Player attack area: x: 200~600, y: 350~650
results = []
for i, fp in enumerate(frames):
    im = Image.open(fp).convert("RGB")
    arr = np.array(im)
    
    # Check enemy area for damage numbers and BREAK
    enemy_crop = arr[80:380, 700:1150]
    # Yellow / Gold (BREAK): R > 200, G > 160, B < 80
    gold_pixels = np.sum((enemy_crop[:,:,0] > 200) & (enemy_crop[:,:,1] > 160) & (enemy_crop[:,:,2] < 80))
    # Red damage: R > 190, G < 130, B < 130
    red_pixels = np.sum((enemy_crop[:,:,0] > 190) & (enemy_crop[:,:,1] < 130) & (enemy_crop[:,:,2] < 130))
    
    # Check player lunge / attack area: player pos diff vs frame 1
    player_crop = arr[350:650, 150:600]
    results.append((i+1, os.path.basename(fp), gold_pixels, red_pixels))

print("Frames with highest gold (BREAK) pixels:")
sorted_gold = sorted(results, key=lambda x: x[2], reverse=True)[:10]
for r in sorted_gold:
    print(f"  Frame {r[0]} ({r[1]}): gold={r[2]}, red={r[3]}")

print("Frames with highest red (Damage) pixels:")
sorted_red = sorted(results, key=lambda x: x[3], reverse=True)[:10]
for r in sorted_red:
    print(f"  Frame {r[0]} ({r[1]}): gold={r[2]}, red={r[3]}")
