from PIL import Image
import numpy as np

f10 = Image.open("/opt/side/bravesoul-game/proofs/combat_feel/macaque_real_01_idle_f0010.png").convert("RGBA")
arr10 = np.array(f10)

crop10 = arr10[380:501, 150:431]
r = crop10[:, :, 0].astype(int)
g = crop10[:, :, 1].astype(int)
b = crop10[:, :, 2].astype(int)
steel = (r > 185) & (g > 185) & (b > 185) & (np.abs(r - b) < 40)

# Where are the steel pixels inside the crop [0..120, 0..280]?
ys, xs = np.where(steel)
print(f"Inside crop (y380..500, x150..430):")
print(f"Total steel pixels: {len(ys)}")
print(f"Y relative to 380: [{ys.min()}..{ys.max()}], absolute Y: [{ys.min()+380}..{ys.max()+380}]")
print(f"X relative to 150: [{xs.min()}..{xs.max()}], absolute X: [{xs.min()+150}..{xs.max()+150}]")

# Let's save a visual mask of these steel pixels on f10
mask_vis = Image.new("RGBA", (281, 121), (0, 0, 0, 0))
for y, x in zip(ys, xs):
    mask_vis.putpixel((x, y), (255, 0, 0, 255))
mask_vis.save("/tmp/f10_steel_mask.png")
print("Saved /tmp/f10_steel_mask.png")
