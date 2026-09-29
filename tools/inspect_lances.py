#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_bfb84d21"
for rel in [
    'game/assets/sprites/player/paperdoll/swan/weapon/weapon_swan_octave_spiral_lance.png',
    'game/assets/sprites/player/paperdoll/sailfish/weapon/weapon_sailfish_hydrofoil_lance.png',
    'game/assets/sprites/player/paperdoll/hippo/weapon/weapon_hippo_steamvalve_piston_heavy_lance.png',
    'game/assets/sprites/player/paperdoll/lion/weapon/wpn_knight_lance.png'
]:
    p = os.path.join(REPO, rel)
    if os.path.exists(p):
        im = Image.open(p)
        box = im.getbbox()
        arr = np.array(im)
        px = int(np.sum(arr[:, :, 3] > 8))
        print(f"{rel}: bbox={box}, pixels={px}")
