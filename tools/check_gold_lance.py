#!/usr/bin/env python3
from typing import cast
from PIL import Image

gold = Image.open("game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold.png").convert("RGBA")
lance = Image.open("game/assets/sprites/player/paperdoll/lion/weapon/wpn_knight_lance.png").convert("RGBA")

print("Gold bbox:", gold.getbbox())
print("Lance bbox:", lance.getbbox())

# Let's check gold pixels at X < 38
gold_left = [cast(tuple[int, int, int, int], gold.getpixel((x, y))) for y in range(128) for x in range(38) if cast(tuple[int, int, int, int], gold.getpixel((x, y)))[3] > 0]
print("Gold pixels with X < 38:", len(gold_left))
