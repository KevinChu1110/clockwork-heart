from PIL import Image
import numpy as np

im_t = Image.open("game/assets/sprites/player/showcase/tortoise_idle_hd.png")
print("tortoise_idle_hd bbox:", im_t.getbbox())
arr_t = np.array(im_t)
print("alpha min:", arr_t[:,:,3].min(), "max:", arr_t[:,:,3].max())

# Compare with branding/char_tortoise.png
im_b = Image.open("branding/char_tortoise.png")
print("branding/char_tortoise size:", im_b.size, "mode:", im_b.mode)
arr_b = np.array(im_b)

# check difference in RGB channels where alpha == 255
diff = np.abs(arr_t[:,:,:3].astype(int) - arr_b.astype(int))
print("diff max:", diff.max(), "diff mean:", diff.mean())

# check what was made transparent in tortoise_idle_hd
transparent_mask = (arr_t[:,:,3] == 0)
print("transparent pixels count:", transparent_mask.sum())
print("sample transparent pixel in char_tortoise:", arr_b[0, 0])
