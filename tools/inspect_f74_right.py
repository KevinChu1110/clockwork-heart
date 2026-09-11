from PIL import Image
import numpy as np

f74 = Image.open("/opt/side/bravesoul-game/proofs/macaque_frames/f_0074.png").convert("RGB")
arr = np.array(f74)

# inspect x in [1270, 1280]
right10 = arr[:, -10:, :]
r = right10[:, :, 0].astype(int)
g = right10[:, :, 1].astype(int)
b = right10[:, :, 2].astype(int)
yellow = (r > 200) & (g > 160) & (b < 100)

ys, xs = np.where(yellow)
print(f"Yellow pixels in right 10px: {len(ys)}")
if len(ys) > 0:
    print(f"Y range: [{ys.min()}..{ys.max()}], X range (rel to 1270): [{xs.min()}..{xs.max()}]")
    # Let's crop a window around these pixels and save it
    crop = f74.crop((1150, ys.min() - 20, 1280, ys.max() + 20))
    crop.save("/tmp/f74_yellow_crop.png")
    print("Saved /tmp/f74_yellow_crop.png")
