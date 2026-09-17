import numpy as np
from PIL import Image

p = 'game/assets/sprites/player/paperdoll/fox/chassis/paint_fox_orange_512.png'
img = Image.open(p).convert('RGBA')
arr = np.array(img)

# 0-QA16 check: alpha > 250 and min(rgb) >= 225
mask = (arr[:, :, 3] > 250) & (np.min(arr[:, :, :3], axis=2) >= 225)
white_pixel_count = np.sum(mask)

# Find maximum horizontal run
max_run = 0
max_run_y = -1
for y in range(512):
    row = mask[y]
    curr_run = 0
    for val in row:
        if val:
            curr_run += 1
            if curr_run > max_run:
                max_run = curr_run
                max_run_y = y
        else:
            curr_run = 0

print(f"File: {p}")
print(f"Total white/near-white pixels (alpha>250, min(rgb)>=225): {white_pixel_count} / {512*512} ({white_pixel_count/(512*512)*100:.3f}%)")
print(f"Max horizontal run of white pixels: {max_run} px (at y={max_run_y})")

# Check source 128 as well
src_p = 'game/assets/sprites/player/paperdoll/fox/chassis/paint_fox_orange.png'
src_arr = np.array(Image.open(src_p).convert('RGBA'))
src_mask = (src_arr[:, :, 3] > 250) & (np.min(src_arr[:, :, :3], axis=2) >= 225)
print(f"Source 128: total white pixels = {np.sum(src_mask)}")
