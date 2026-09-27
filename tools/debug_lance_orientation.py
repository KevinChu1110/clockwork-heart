#!/usr/bin/env python3
from PIL import Image, ImageOps
import numpy as np

wpn = Image.open('/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/hound/weapon/weapon_hound_stellar_beacon_lance.png').convert('RGBA')
bbox = wpn.getbbox()
lance_raw = wpn.crop(bbox)

def place_lance(lance_img: Image.Image, deg: float, target_center: tuple[int, int], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    b = lance_img.copy()
    if mirror:
        b = ImageOps.mirror(b)
    bw, bh = b.size
    gx, gy = bw / 2.0, bh / 2.0

    canvas_size = 256
    large = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    large.paste(b, (int(round(128 - gx)), int(round(128 - gy))))

    if scale != 1.0:
        nw = int(round(canvas_size * scale))
        nh = int(round(canvas_size * scale))
        scaled = large.resize((nw, nh), Image.Resampling.LANCZOS)
        offset = (nw - canvas_size) // 2
        large = scaled.crop((offset, offset, offset + canvas_size, offset + canvas_size))

    rotated = large.rotate(deg, resample=Image.Resampling.BICUBIC, center=(128, 128))
    out = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tx, ty = target_center
    out.paste(rotated, (tx - 128, ty - 128), rotated)
    return out

# In idle, weapon_src is at its canonical position:
# Tip is at (4, 42), grip at (28, 74), counterweight at (48, 88).
# Notice: tip is on LEFT (x=4), grip is at center (x=28), counterweight is at RIGHT (x=48)!
# So in raw lance, the lance points to the LEFT!
print("Raw lance points to the LEFT (x=4..48, y=42..88)!")
