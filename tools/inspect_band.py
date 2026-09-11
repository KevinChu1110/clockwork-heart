from PIL import Image
import numpy as np

im = Image.open("screenshots/proof_battle_lion_full_screen.png")
# Let's crop y from 350 to 450, x from 0 to 1280
crop = im.crop((0, 350, 1280, 450))
crop.save("/tmp/proof_band.png")
print("Saved /tmp/proof_band.png")

# Also find where the dark pixels (L < 70) are located in x for y in range(383, 391)
lim = im.convert("L")
arr = np.array(lim)
for y in range(383, 391):
    xs = np.where(arr[y, :] < 70)[0]
    print(f"y={y}: count={len(xs)}, min_x={xs.min() if len(xs) else None}, max_x={xs.max() if len(xs) else None}")
