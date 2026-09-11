from PIL import Image
import numpy as np

im = Image.open("screenshots/proof_battle_lion_full_screen.png")
lim = im.convert("L")
arr = np.array(lim)

y = 384
print("Total dark at y=384:", (arr[y, :] < 70).sum())

# What is on screen at y=384?
# Let's inspect where dark pixels are:
dark_xs = np.where(arr[y, :] < 70)[0]

# Let's check rabbit screenshot at y=384
im_rab = Image.open("screenshots/proof_battle_full_screen.png").convert("L")
arr_rab = np.array(im_rab)
print("Rabbit dark at y=384:", (arr_rab[y, :] < 70).sum())

# Print ranges of x in lion vs rabbit
diff = (arr[y, :] < 70) != (arr_rab[y, :] < 70)
diff_indices = np.where(diff)[0]
print("Indices where lion differs from rabbit at y=384:", diff_indices)
