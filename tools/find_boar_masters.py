#!/usr/bin/env python3
import os

candidates = [
    "/opt/side/bravesoul-game/proofs/debug_hd_in_512.png",
    "/root/boar_master_512.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/proof_paperdoll_boar_composite.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/proof_chassis_swap_boar.png"
]

for c in candidates:
    if os.path.exists(c):
        print("EXISTS:", c)
    else:
        print("MISSING:", c)
