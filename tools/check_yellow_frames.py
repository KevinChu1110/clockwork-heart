from PIL import Image
import numpy as np

# Let's inspect f_0024..f_0035 on the right side
frame_dir = "/opt/side/bravesoul-game/proofs/macaque_frames"

for i in range(22, 35):
    fn = f"f_{i:04d}.png"
    im = Image.open(f"{frame_dir}/{fn}").convert("RGB")
    arr = np.array(im)
    # Leo area: x in [700, 1280], y in [150, 600]
    sub = arr[150:600, 700:1280]
    r = sub[:, :, 0].astype(int)
    g = sub[:, :, 1].astype(int)
    b = sub[:, :, 2].astype(int)
    # yellow text: r>200, g>160, b<100
    yellow = (r > 200) & (g > 160) & (b < 100)
    cnt = np.count_nonzero(yellow)
    print(f"Frame {i:2d} ({fn}): Leo area yellow pixels = {cnt}")

# What about frames 70..90?
for i in range(70, 91):
    fn = f"f_{i:04d}.png"
    im = Image.open(f"{frame_dir}/{fn}").convert("RGB")
    arr = np.array(im)
    sub = arr[150:600, 700:1280]
    r = sub[:, :, 0].astype(int)
    g = sub[:, :, 1].astype(int)
    b = sub[:, :, 2].astype(int)
    yellow = (r > 200) & (g > 160) & (b < 100)
    cnt = np.count_nonzero(yellow)
    print(f"Frame {i:2d} ({fn}): Leo area yellow pixels = {cnt}")
