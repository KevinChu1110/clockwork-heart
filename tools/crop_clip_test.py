#!/usr/bin/env python3
from PIL import Image

for name in ["test_clip_true", "test_clip_false"]:
    im = Image.open(f"/tmp/{name}.png")
    # crop LogPanel top: y=520~610, x=20~800
    crop = im.crop((20, 520, 800, 610))
    crop.save(f"/tmp/{name}_crop.png")

print("Saved crops.")
