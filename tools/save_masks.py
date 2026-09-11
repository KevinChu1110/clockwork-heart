from PIL import Image
import numpy as np

im_lion = Image.open("screenshots/proof_battle_lion_full_screen.png").convert("L")
im_rab = Image.open("screenshots/proof_battle_full_screen.png").convert("L")

arr_l = np.array(im_lion)
arr_r = np.array(im_rab)

mask_l = ((arr_l < 70) * 255).astype(np.uint8)
mask_r = ((arr_r < 70) * 255).astype(np.uint8)

Image.fromarray(mask_l).save("/tmp/mask_lion.png")
Image.fromarray(mask_r).save("/tmp/mask_rab.png")
print("Saved masks")
