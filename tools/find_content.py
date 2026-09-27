from PIL import Image
import numpy as np

im = Image.open("/tmp/test_http_1280.png")
print("Total size:", im.size)

# Scan horizontal slices of 100px height and check max brightness or variation
arr = np.array(im)
for y in range(0, im.size[1], 200):
    slice_arr = arr[y:y+200, :, :]
    max_val = slice_arr.max()
    min_val = slice_arr.min()
    mean_val = slice_arr.mean()
    std_val = slice_arr.std()
    print(f"y={y:4d}..{y+200:4d}: min={min_val:3d}, max={max_val:3d}, mean={mean_val:5.1f}, std={std_val:5.1f}")
