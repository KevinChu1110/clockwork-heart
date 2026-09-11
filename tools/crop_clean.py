#!/usr/bin/env python3
from PIL import Image

im = Image.open("/tmp/cleaned_paint_ivory_stock.png")
crop_face = im.crop((35, 20, 95, 60))
crop_face.save("/tmp/clean_face.png")
crop_torso = im.crop((35, 60, 95, 110))
crop_torso.save("/tmp/clean_torso.png")
print("Saved /tmp/clean_face.png and /tmp/clean_torso.png")
