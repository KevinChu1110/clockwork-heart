#!/usr/bin/env python3
from PIL import Image

im = Image.open("/tmp/test_clean_bamboo_bronze.png").convert("RGBA")
w, h = im.size

# Find connected components of opaque pixels:
from scipy.ndimage import label
import numpy as np

arr = np.array(im)[:, :, 3] > 0
labeled, num_features = label(arr)
print(f"Number of connected components: {num_features}")

# Print component sizes:
sizes = [(labeled == i).sum() for i in range(1, num_features + 1)]
for i, s in enumerate(sizes, 1):
    if s < 50:
        coords = np.argwhere(labeled == i)
        print(f"Component {i} (size {s}): min_y={coords[:,0].min()}, max_y={coords[:,0].max()}, min_x={coords[:,1].min()}, max_x={coords[:,1].max()}")
        for y, x in coords:
            print(f"  ({x}, {y}): rgba={im.getpixel((int(x), int(y)))}")
