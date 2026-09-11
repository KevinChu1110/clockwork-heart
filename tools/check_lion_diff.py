import numpy as np
from PIL import Image, ImageChops

im0 = Image.open("/tmp/test_idle_lion_0.png").convert("RGBA")
im1 = Image.open("/tmp/test_idle_lion_1.png").convert("RGBA")

diff = ImageChops.difference(im0, im1)
bbox = diff.getbbox(alpha_only=False)
arr0 = np.array(im0)
arr1 = np.array(im1)
diff_mask = np.any(arr0 != arr1, axis=2)
diff_px = int(np.sum(diff_mask))
print("Lion 128x128 diff bbox:", bbox, "diff px:", diff_px)
