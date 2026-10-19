#!/usr/bin/env python3
import os, shutil

paths = [
    "/opt/side/bravesoul-game/game/data/tables/maple_paperdoll_macaque.json",
    "/opt/side/bravesoul-game/tools/build_macaque_maple_paperdoll.py"
]

for p in paths:
    if os.path.exists(p):
        os.remove(p)
        print(f"Removed {p}")

macaque_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque"
if os.path.exists(macaque_dir):
    shutil.rmtree(macaque_dir)
    print(f"Removed {macaque_dir}")
