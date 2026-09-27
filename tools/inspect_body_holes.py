import numpy as np
from PIL import Image

for race in ["squirrel", "otter", "hedgehog", "raccoon", "kangaroo"]:
    p = f"game/assets/sprites/player/paperdoll/{race}/proof_paperdoll_{race}_magenta.png"
    mag_im = Image.open(p).convert("RGB")
    mag_arr = np.array(mag_im)
    body_crop = mag_arr[35:90, 48:78]
    is_mag = (body_crop[:, :, 0] == 255) & (body_crop[:, :, 1] == 0) & (body_crop[:, :, 2] == 255)
    print(f"{race:10s} magenta pixels in body crop (x:48..78, y:35..90): {np.sum(is_mag)}")
