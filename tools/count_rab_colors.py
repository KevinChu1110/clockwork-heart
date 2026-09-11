#!/usr/bin/env python3
from PIL import Image

rab = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit/chassis/paint_ivory_stock.png").convert("RGBA")
pixels = [rab.getpixel((x, y)) for y in range(rab.height) for x in range(rab.width) if rab.getpixel((x, y))[3] > 0]
u_cols = set(pixels)
print(f"Rabbit chassis: {len(pixels)} opaque pixels, {len(u_cols)} unique colors!")
print(f"Ratio colors / pixels: {len(u_cols) / len(pixels):.3f}")
