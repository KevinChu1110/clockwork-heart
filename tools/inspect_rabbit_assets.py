import os
from PIL import Image

rabbit_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit"
for root, dirs, files in os.walk(rabbit_dir):
    for f in sorted(files):
        if f.endswith(".png"):
            p = os.path.join(root, f)
            im = Image.open(p)
            print(f"{os.path.relpath(p, rabbit_dir)}: size={im.size} mode={im.mode}")
