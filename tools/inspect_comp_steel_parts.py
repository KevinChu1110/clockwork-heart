from PIL import Image
import numpy as np

comp = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/proof_paperdoll_macaque_composite.png").convert("RGBA")
arr = np.array(comp)

# Find all steel pixels in y in [83..128]
steel = (arr[:, :, 3] > 128) & (arr[:, :, 0] > 185) & (arr[:, :, 1] > 185) & (arr[:, :, 2] > 185) & (np.abs(arr[:, :, 0].astype(int) - arr[:, :, 2].astype(int)) < 40)
ys, xs = np.where(steel & (np.arange(128)[:, None] >= 83))

print(f"Total steel in comp y >= 83: {len(ys)}")
print(f"X range: [{xs.min()}..{xs.max()}], Y range: [{ys.min()}..{ys.max()}]")

# Let's save these pixels on comp to an image so we see what body parts they are!
vis = comp.copy()
for y, x in zip(ys, xs):
    vis.putpixel((x, y), (255, 0, 0, 255))
vis.save("/tmp/comp_steel_parts.png")
print("Saved /tmp/comp_steel_parts.png")
