from PIL import Image, ImageChops
import numpy as np

im_a = Image.open('/tmp/test_macaque_comp_a.png').convert('RGBA')
im_b = Image.open('/tmp/test_macaque_comp_b.png').convert('RGBA')

diff = ImageChops.difference(im_a, im_b)
bbox = diff.getbbox(alpha_only=False)
print("BBox (alpha_only=False):", bbox)

arr_a = np.array(im_a)
arr_b = np.array(im_b)
diff_mask = np.any(arr_a != arr_b, axis=2)
diff_px = int(np.sum(diff_mask))
print("Diff pixels:", diff_px)
