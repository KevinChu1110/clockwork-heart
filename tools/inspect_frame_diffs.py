import os
import glob
import numpy as np
from PIL import Image

tmp = "/tmp/macaque_all_frames"
frames = sorted(glob.glob(f"{tmp}/f_*.png"))
f0 = np.array(Image.open(frames[0]).convert("RGB"), dtype=np.float32)

print("Frame differences vs frame 1:")
for i in range(0, len(frames), 5):
    fi = np.array(Image.open(frames[i]).convert("RGB"), dtype=np.float32)
    diff = np.abs(f0 - fi).mean()
    p_diff = np.abs(f0[350:650, 150:600] - fi[350:650, 150:600]).mean()
    e_diff = np.abs(f0[80:450, 700:1150] - fi[80:450, 700:1150]).mean()
    print(f"Frame {i+1:3d}: total_diff={diff:5.2f}, player_area={p_diff:5.2f}, enemy_area={e_diff:5.2f}")
