import os
from PIL import Image

for root, dirs, files in os.walk("/opt/side/bravesoul-game/web/media"):
    for f in files:
        if f.endswith(".png") and "char_" in f:
            p = os.path.join(root, f)
            img = Image.open(p)
            print(f, img.mode, img.size, img.getpixel((0,0)))
