#!/usr/bin/env python3
from PIL import Image, ImageOps

BASE = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise"
wpn = Image.open(f"{BASE}/weapon/wpn_bagua_astrolabe.png").convert("RGBA")
wb = wpn.crop(wpn.getbbox())

def place_astrolabe(astrolabe_img: Image.Image, deg: float, target_center: tuple[int, int], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    b = astrolabe_img.copy()
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

placed = place_astrolabe(wb, 0, (96, 62), 1.0)
print(f"Original wpn bbox: {wpn.getbbox()}")
print(f"Placed wpn bbox:   {placed.getbbox()}")
