#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

shot_dir = "/opt/side/bravesoul-game/screenshots"
for fn in [
    "proof_battle_boar_full_screen.png",
    "proof_battle_boar_attack_full_screen.png",
    "proof_battle_boar_equipped_ironclad.png",
    "proof_battle_boar_equipped_harness.png",
    "proof_battle_boar_attack_hammer.png"
]:
    p = os.path.join(shot_dir, fn)
    sim = Image.open(p).convert("L")
    sarr = np.array(sim)
    h, w = sim.size[1], sim.size[0]
    max_streak = 0
    max_y = -1
    for y in range(int(h * 0.35), int(h * 0.55)):
        streak = 0
        cur_max = 0
        for x in range(240, min(w, 460)):
            if sarr[y, x] < 70:
                streak += 1
                if streak > cur_max:
                    cur_max = streak
            else:
                streak = 0
        if cur_max > max_streak:
            max_streak = cur_max
            max_y = y
    print(f"{fn}: max_streak={max_streak} (at y={max_y}, h={h}, w={w})")
