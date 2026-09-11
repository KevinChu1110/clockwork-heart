from PIL import Image
import numpy as np

for p in ["/tmp/lion_nutcracker_full.png", "/tmp/lion_nutcracker_atk_full.png"]:
    sim = Image.open(p).convert("L")
    sarr = np.array(sim)
    h, w = sim.size[1], sim.size[0]
    bad = []
    for y in range(h):
        cnt = (sarr[y, :] < 70).sum()
        if cnt > w * 0.35 and 0.35 <= y / float(h) <= 0.55:
            bad.append((y, cnt))
    print(f"{p}: bad={len(bad)}, max_cnt={max((sarr[y, :] < 70).sum() for y in range(int(h*0.35), int(h*0.55)))}")
