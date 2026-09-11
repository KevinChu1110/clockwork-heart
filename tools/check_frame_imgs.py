import os
import glob
from PIL import Image

tmp = "/tmp/macaque_all_frames"
frames = [10, 20, 75, 78, 80, 82, 85, 90, 100]

for f in frames:
    p = f"{tmp}/f_{f:04d}.png"
    if os.path.exists(p):
        im = Image.open(p)
        print(f"Frame {f}: size={im.size}")
