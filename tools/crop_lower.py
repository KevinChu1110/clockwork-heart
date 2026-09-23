#!/usr/bin/env python3
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/docs/art/xuanji_tortoise_concept.png").convert("RGBA")
flipped = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
cropped = flipped.crop((250, 550, 950, 715))
cropped.save("/tmp/tortoise_lower_body.png")
print("Saved /tmp/tortoise_lower_body.png")
