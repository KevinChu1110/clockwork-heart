#!/usr/bin/env python3
from PIL import Image, ImageOps, ImageDraw

wpn = Image.open('/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/hound/weapon/weapon_hound_stellar_beacon_lance.png').convert('RGBA')
bbox = wpn.getbbox()
assert bbox is not None
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

# Test attack with mirror=True:
# When mirrored: tip is at RIGHT, grip is at (bw - 24, 32), counterweight is at LEFT!
# deg=0: tip points right-up
# deg=-25: tip points straight forward right!
test_atk_lance = place_lance(lance_raw, deg=-25, target_center=(68, 68), scale=1.08, mirror=True)
print("Attack lance mirrored bbox:", test_atk_lance.getbbox())
