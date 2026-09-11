#!/usr/bin/env python3
from PIL import Image

im = Image.open("/tmp/test_snapped_28.png")
crop = im.crop((20, 520, 800, 610))
crop.save("/tmp/test_snapped_28_crop.png")
print("Saved 28 crop.")
