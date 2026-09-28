#!/usr/bin/env python3
from typing import cast
from PIL import Image, ImageChops

REPO_ROOT = "/opt/side/bravesoul-game"
idle_128 = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/poses/courser/idle.png").convert("RGBA")
attack_128 = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/poses/courser/attack.png").convert("RGBA")

diff_b = ImageChops.difference(idle_128, attack_128)
ch_b = sum(1 for y in range(128) for x in range(128) if any(c > 0 for c in cast(tuple[int, int, int, int], diff_b.getpixel((x, y)))))
diff_legs = ImageChops.difference(idle_128.crop((0, 88, 128, 128)), attack_128.crop((0, 88, 128, 128)))
ch_legs = sum(1 for y in range(40) for x in range(128) if any(c > 0 for c in cast(tuple[int, int, int, int], diff_legs.getpixel((x, y)))))

print(f"ch_b (total diff): {ch_b} ({ch_b / (128*128) * 100:.1f}%)")
print(f"ch_legs (lower body diff): {ch_legs}")

bbox_b = attack_128.getbbox()
print(f"attack_128 bbox: {bbox_b}, margins: L={bbox_b[0]}, R={128-bbox_b[2]}, T={bbox_b[1]}, B={128-bbox_b[3]}")
