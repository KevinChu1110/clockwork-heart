#!/usr/bin/env python3
from PIL import Image

im = Image.open("/tmp/repaired_ivory_stock.png")
im.crop((35, 20, 95, 60)).save("/tmp/repaired_face.png")
im.crop((35, 60, 95, 110)).save("/tmp/repaired_torso.png")
print("Saved /tmp/repaired_face.png and /tmp/repaired_torso.png")
