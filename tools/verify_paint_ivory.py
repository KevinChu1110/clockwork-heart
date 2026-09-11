#!/usr/bin/env python3
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png").convert("RGBA")
# Check the eye crack:
print("Eye crack check (68, 34):", im.getpixel((68, 34)))
print("Eye crack check (70, 39):", im.getpixel((70, 39)))
print("Cheek crack check (78, 33):", im.getpixel((78, 33)))
print("Belly scratch (53, 82):", im.getpixel((53, 82)))
