from PIL import Image
import numpy as np

for name in ["gi.png", "cloth.png", "veil.png", "leather.png", "plate.png", "hide.png"]:
    im = Image.open(f"/opt/side/bravesoul-game/game/assets/sprites/player/armor/{name}")
    print(name, im.size, im.mode)
