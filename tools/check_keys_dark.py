import numpy as np
from PIL import Image

for race in ["squirrel", "otter", "hedgehog", "raccoon", "kangaroo", "wolf", "seahorse", "cat"]:
    path = f"game/assets/sprites/player/paperdoll/{race}/winding_key/"
    import os
    if not os.path.exists(path): continue
    for f in os.listdir(path):
        if f.endswith(".png") and not f.endswith("_512.png"):
            im = Image.open(f"{path}/{f}").convert("RGBA")
            arr = np.array(im)
            alpha = arr[:, :, 3]
            dark = (alpha > 8) & (arr[:, :, 0] < 90) & (arr[:, :, 1] < 90) & (arr[:, :, 2] < 130)
            cnt = np.sum(dark)
            max_run = 0
            rows_20 = 0
            for r in range(128):
                cur = 0
                rm = 0
                for v in dark[r, :]:
                    if v:
                        cur += 1
                        rm = max(rm, cur)
                    else:
                        cur = 0
                max_run = max(max_run, rm)
                if rm >= 20: rows_20 += 1
            print(f"{race:10s} {f[:35]:35s}: dark={cnt:4d}, max_run={max_run:2d}, rows_run>=20={rows_20}")
