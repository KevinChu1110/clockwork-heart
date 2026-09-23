#!/usr/bin/env python3
import os
from PIL import Image

def check_race(race):
    base_dir = f"/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/{race}"
    print(f"=== Checking {race} ===")
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.endswith(".png") and not f.endswith("_512.png") and not f.startswith("proof") and not f.startswith("verification"):
                p = os.path.join(root, f)
                im = Image.open(p)
                bbox = im.getbbox()
                print(f"  {os.path.relpath(p, base_dir)}: size={im.size}, bbox={bbox}")

if __name__ == "__main__":
    check_race("penguin")
    check_race("bear")
    check_race("crane")
