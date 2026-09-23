import os
from PIL import Image

for f in sorted(os.listdir("game/assets/sprites/player/showcase")):
    if f.endswith("_idle_hd.png"):
        im = Image.open(f"game/assets/sprites/player/showcase/{f}")
        print(f, im.size, im.mode)
