from PIL import Image
import numpy as np

for r in ["fox", "boar", "macaque"]:
    p = f"/tmp/{r}_test_fullscreen.png"
    sim = Image.open(p).convert("L")
    sarr = np.array(sim)
    h, w = sim.size[1], sim.size[0]
    bad = []
    for y in range(h):
        cnt = (sarr[y, :] < 70).sum()
        if cnt > w * 0.35 and 0.35 <= y / float(h) <= 0.55:
            bad.append((y, cnt))
    max_c = max((sarr[y, :] < 70).sum() for y in range(int(h*0.35), int(h*0.55)))
    print(f"{r}: bad={len(bad)}, max_cnt={max_c} (threshold w*0.35={w*0.35})")
