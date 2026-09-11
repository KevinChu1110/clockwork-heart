#!/usr/bin/env python3
import sys
import os
import math
from typing import cast
from PIL import Image

staff_src = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
clean_staff = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = staff_src.load()
cs_px = clean_staff.load()
assert s_px is not None and cs_px is not None
for y in range(128):
    for x in range(128):
        if 80 <= x <= 112 and 38 <= y <= 125:
            cs_px[x, y] = cast(tuple[int, int, int, int], s_px[x, y])

def place_rigid_staff(staff_img: Image.Image, deg: float, target_hand: tuple[int, int], scale: float = 1.0) -> Image.Image:
    large_canvas = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    large_canvas.paste(staff_img, (128 - 93, 128 - 88))
    if scale != 1.0:
        sw = int(round(256 * scale))
        sh = int(round(256 * scale))
        large_canvas = large_canvas.resize((sw, sh), Image.Resampling.LANCZOS)
    rotated = large_canvas.rotate(deg, resample=Image.Resampling.BICUBIC, center=(128, 128))
    out_128 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hx, hy = target_hand
    out_128.paste(rotated, (hx - 128, hy - 128), rotated)
    return out_128

# Let's inspect where pixels in (105..123, 27..37) come from in clean_staff!
# reverse mapping:
# fx = 114, fy = 32
# fx = rx - 128 + 84 => rx = fx - 84 + 128 = 114 - 84 + 128 = 158
# fy = ry - 128 + 58 => ry = fy - 58 + 128 = 32 - 58 + 128 = 102
# rotated by -65 deg: to unrotate, rotate by +65 deg!
rad = math.radians(65)
cos_a = math.cos(rad)
sin_a = math.sin(rad)

for fx, fy in [(114, 32), (106, 30), (120, 35)]:
    rx = fx - 84 + 128
    ry = fy - 58 + 128
    lx = 128 + cos_a * (rx - 128) - sin_a * (ry - 128)
    ly = 128 + sin_a * (rx - 128) + cos_a * (ry - 128)
    sx = (lx - 128) / 0.98 + 93
    sy = (ly - 128) / 0.98 + 88
    print(f"out_128 ({fx},{fy}) mapped to clean_staff approx ({sx:.1f}, {sy:.1f})")
