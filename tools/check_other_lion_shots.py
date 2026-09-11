from PIL import Image
import numpy as np

for sp in ["screenshots/proof_battle_lion_equipped_nutcracker_guard.png", "screenshots/proof_battle_lion_equipped_steam_artisan.png", "screenshots/proof_battle_lion_attack_full_screen.png", "screenshots/proof_battle_lion_attack_lance.png"]:
    sim = Image.open(sp).convert("L")
    sarr = np.array(sim)
    h, w = sim.size[1], sim.size[0]
    bad = []
    for y in range(h):
        cnt = (sarr[y, :] < 70).sum()
        if cnt > w * 0.35 and 0.35 <= y / float(h) <= 0.55:
            bad.append((y, cnt))
    print(f"{sp}: bad={len(bad)}, max_cnt={max((sarr[y, :] < 70).sum() for y in range(int(h*0.35), int(h*0.55)))}")
