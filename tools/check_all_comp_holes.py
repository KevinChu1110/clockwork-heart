import numpy as np
from PIL import Image
from scipy.ndimage import binary_fill_holes

for race in ["otter", "hedgehog", "raccoon", "kangaroo", "wolf", "seahorse", "cat"]:
    p = f"game/assets/sprites/player/paperdoll/{race}/proof_paperdoll_{race}_composite.png"
    import os
    if not os.path.exists(p): continue
    comp_im = Image.open(p).convert("RGBA")
    comp_arr = np.array(comp_im)
    comp_alpha = comp_arr[:, :, 3] > 8
    filled = binary_fill_holes(comp_alpha)
    holes = filled & (~comp_alpha)
    print(f"{race:10s} composite hole pixels: {np.sum(holes)}")
