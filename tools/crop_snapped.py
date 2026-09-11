#!/usr/bin/env python3
from PIL import Image

im = Image.open("/tmp/test_snapped.png")
crop = im.crop((20, 520, 800, 610))
crop.save("/tmp/test_snapped_crop.png")
print("Saved crop.")
