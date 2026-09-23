from PIL import Image
import numpy as np

im = Image.open("game/assets/sprites/player/showcase/tortoise_idle_hd.png")
arr = np.array(im)
print("tortoise_idle_hd size:", im.size, "bbox:", im.getbbox())
# Let's inspect rows around feet/shadow: bbox bottom is 1604
shadow_rows = arr[1550:1610, :, 3]
print("alpha around bottom max:", shadow_rows.max(axis=1))
# does it have soft shadow at the bottom?
print("RGB of bottom pixels where alpha > 0:")
mask = (arr[1580:1610, :, 3] > 0) & (arr[1580:1610, :, 3] < 200)
if np.any(mask):
    print("semi-transparent RGB sample:", arr[1580:1610, :, :3][mask][:5])
    print("semi-transparent Alpha sample:", arr[1580:1610, :, 3][mask][:5])
