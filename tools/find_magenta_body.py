import numpy as np
from PIL import Image

mag_im = Image.open("game/assets/sprites/player/paperdoll/squirrel/proof_paperdoll_squirrel_magenta.png").convert("RGB")
mag_arr = np.array(mag_im)
body_crop = mag_arr[35:90, 48:78]
is_mag = (body_crop[:, :, 0] == 255) & (body_crop[:, :, 1] == 0) & (body_crop[:, :, 2] == 255)
coords = np.argwhere(is_mag)
for y_rel, x_rel in coords:
    print(f"y={35 + y_rel}, x={48 + x_rel}")
