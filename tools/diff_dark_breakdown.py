from PIL import Image
import numpy as np

im_lion = Image.open("screenshots/proof_battle_lion_full_screen.png").convert("L")
im_rab = Image.open("screenshots/proof_battle_full_screen.png").convert("L")

arr_l = np.array(im_lion)
arr_r = np.array(im_rab)

y = 384
diff_xs = []
for x in range(1280):
    val_l = arr_l[y, x] < 70
    val_r = arr_r[y, x] < 70
    if val_l and not val_r:
        diff_xs.append(x)

print(f"Number of extra dark pixels in lion at y=384: {len(diff_xs)}")
print(f"X range of extra dark pixels: min={min(diff_xs) if diff_xs else None}, max={max(diff_xs) if diff_xs else None}")

# Print x coordinates where diff_xs occurs
import collections
hist = collections.defaultdict(int)
for x in diff_xs:
    hist[x // 50 * 50] += 1
for k in sorted(hist.keys()):
    print(f"x in [{k}, {k+49}]: {hist[k]}")
