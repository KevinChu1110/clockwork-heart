import os
from PIL import Image, ImageChops

base_im = Image.open("/tmp/rabbit_frames/frame_001.png")
for i in range(2, 91):
    cur_im = Image.open(f"/tmp/rabbit_frames/frame_{i:03d}.png")
    diff = ImageChops.difference(base_im, cur_im)
    b = diff.getbbox()
    if b:
        print(f"Frame {i:03d} changed! bbox={b}")
