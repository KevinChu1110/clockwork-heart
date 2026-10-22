#!/usr/bin/env python3
from PIL import Image
import numpy as np

body = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/maple_parts/body/paint_brass_gold.png").convert("RGBA")
arr = np.array(body)

# Check upper-right: x: 300..512, y: 0..250
# Is there an aura in body?
# Look at alpha
print("Body upper right alpha min/max:", np.min(arr[0:250, 300:512, 3]), np.max(arr[0:250, 300:512, 3]))

# Where is alpha between 1 and 250? (translucent aura)
semi = (arr[:, :, 3] > 0) & (arr[:, :, 3] < 250)
print("Body semi-transparent pixel count:", np.sum(semi))

# Let's check where semi-transparent pixels are located
ys, xs = np.where(semi)
if len(ys) > 0:
    print(f"Semi-trans range Y: {ys.min()}..{ys.max()}, X: {xs.min()}..{xs.max()}")

# Let's check if there is an aura or straight cuts in body
for y in range(0, 250):
    for x in range(300, 511):
        if arr[y, x, 3] == 0 and arr[y, x+1, 3] > 100:
            pass

# Also check head
head = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl.png").convert("RGBA")
head_arr = np.array(head)
print("Head size:", head.size)
semi_h = (head_arr[:, :, 3] > 0) & (head_arr[:, :, 3] < 250)
print("Head semi-trans count:", np.sum(semi_h))

# Also check weapon
wpn = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/maple_parts/weapon/wpn_anvil_greathammer.png").convert("RGBA")
wpn_arr = np.array(wpn)
print("Weapon size:", wpn.size)
# Look at bottom-right of weapon
print("Weapon bottom right (y: 200..254, x: 100..167):")
print("Non-zero alpha in wpn:", np.sum(wpn_arr[:, :, 3] > 0))
