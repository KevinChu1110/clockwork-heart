#!/usr/bin/env python3
from PIL import Image, ImageOps
import numpy as np

BASE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/gecko"
key_src = Image.open(f"{BASE_DIR}/winding_key/key_gecko_dual_ring_relief_valve_brass.png").convert("RGBA")
key_raw = key_src.crop(key_src.getbbox())

def place_rotated_element(elem_img: Image.Image, deg: float, target_center: tuple[int, int], scale: float = 1.0) -> Image.Image:
    b = elem_img.copy()
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

for deg in [0, 24, 35, 45, 88]:
    k = place_rotated_element(key_raw, deg=deg, target_center=(72, 26), scale=1.0)
    arr = np.array(k)
    ys, xs = np.where(arr[:, :, 3] > 20)
    print(f"deg={deg:2d}: y=[{ys.min():2d}..{ys.max():2d}], x=[{xs.min():2d}..{xs.max():2d}]")
