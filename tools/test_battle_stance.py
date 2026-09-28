#!/usr/bin/env python3
from typing import cast
from PIL import Image, ImageChops

idle = Image.open("game/assets/sprites/player/poses/kite/idle.png").convert("RGBA")
attack = Image.open("game/assets/sprites/player/poses/kite/attack.png").convert("RGBA")

diff = ImageChops.difference(idle, attack)
ch_b = sum(1 for y in range(128) for x in range(128) if any(c > 0 for c in cast(tuple[int, int, int, int], diff.getpixel((x, y)))))

diff_legs = ImageChops.difference(idle.crop((0, 88, 128, 128)), attack.crop((0, 88, 128, 128)))
ch_legs = sum(1 for y in range(40) for x in range(128) if any(c > 0 for c in cast(tuple[int, int, int, int], diff_legs.getpixel((x, y)))))

bbox = attack.getbbox()
assert bbox is not None
left_m = bbox[0]
right_m = 128 - bbox[2]
top_m = bbox[1]
bot_m = 128 - bbox[3]

print(f"Attack bbox: {bbox}")
print(f"Margins: L={left_m}, T={top_m}, R={right_m}, B={bot_m}")
print(f"Changed pixels vs idle: {ch_b} ({ch_b / (128*128) * 100:.1f}%) [req > 2500px]")
print(f"Changed pixels in legs/pelvis (y>=88): {ch_legs} [req > 500px]")
