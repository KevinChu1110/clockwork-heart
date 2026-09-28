#!/usr/bin/env python3
from PIL import Image, ImageChops
import numpy as np

idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/sailfish/idle.png").convert("RGBA")
attack = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/sailfish/attack.png").convert("RGBA")

diff = ImageChops.difference(idle, attack)
ch = sum(1 for y in range(128) for x in range(128) if any(c > 0 for c in diff.getpixel((x, y))))
diff_legs = ImageChops.difference(idle.crop((0, 88, 128, 128)), attack.crop((0, 88, 128, 128)))
ch_legs = sum(1 for y in range(40) for x in range(128) if any(c > 0 for c in diff_legs.getpixel((x, y))))

b_bbox = attack.getbbox()
print("Attack bbox:", b_bbox)
print(f"Left margin: {b_bbox[0]}px, Right margin: {128 - b_bbox[2]}px, Top: {b_bbox[1]}px, Bottom: {128 - b_bbox[3]}px")
print(f"Total diff: {ch}px (requires > 2500px)")
print(f"Legs/tail diff: {ch_legs}px (requires > 500px)")
