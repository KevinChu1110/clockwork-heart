from PIL import Image
import numpy as np

im = Image.open("branding/char_elephant.png")
print("size:", im.size, "mode:", im.mode)
arr = np.array(im)
# background is around [235, 226, 209]
dist = np.max(np.abs(arr.astype(float) - np.array([235., 226., 209.])), axis=2)
non_bg = dist > 10
y_indices, x_indices = np.where(non_bg)
print("non-bg bbox:", x_indices.min(), y_indices.min(), x_indices.max(), y_indices.max())
