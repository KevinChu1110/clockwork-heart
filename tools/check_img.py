from PIL import Image
import os

p = "/opt/side/bravesoul-game/web/media/hero/char_rabbit.png"
if os.path.exists(p):
    img = Image.open(p)
    print("char_rabbit.png:", img.mode, img.size, "corner pixel:", img.getpixel((0,0)))
