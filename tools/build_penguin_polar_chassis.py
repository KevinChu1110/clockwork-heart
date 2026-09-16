#!/usr/bin/env python3
"""
tools/build_penguin_polar_chassis.py
Constructs:
1. paint_polar_frost.png (極光冰川銀白鍍鉻烤漆) for The Steam Penguin paperdoll chassis.
   - Source: game/assets/sprites/player/paperdoll/penguin/chassis/paint_penguin_navy.png
   - Archetype: 遊俠 (Ranger) 淵海火槍手機甲素體
   - Style: 極地破冰高光銀白鍍鉻 (Polar Frost Chrome Enamel) with golden flipper hinges and saturated orange feet.
   - Pure clockwork toy aesthetic: zero fur, zero biological meat, crisp #1F1A3A outline.
   - Fully compliant with review.md 0-ART9 (zero weapons on chassis, flippers completely bare).
   - 128x128 RGBA
2. paint_ivory_stock.png (原廠象牙白高光琺瑯塗層)
   - Consistent warm ivory toy chassis variant.
"""

from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
PENGUIN_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/penguin"

def create_penguin_paint_polar_frost(src_path: str = "", out_path: str = "") -> Image.Image:
    if not src_path:
        src_path = f"{PENGUIN_DIR}/chassis/paint_penguin_navy.png"
    if not out_path:
        out_path = f"{PENGUIN_DIR}/chassis/paint_polar_frost.png"

    navy = Image.open(src_path).convert("RGBA")
    w, h = navy.size
    polar = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    for y in range(h):
        for x in range(w):
            px = cast(tuple[int, int, int, int], navy.getpixel((x, y)))
            r, g, b, a = px
            if a <= 10:
                continue

            # 1. Ground soft shadow at base (Y >= 112)
            if y >= 112 and (r < 50 and g < 50 and b < 80):
                polar.putpixel((x, y), (r, g, b, a))
                continue

            lum = int(0.299 * r + 0.587 * g + 0.114 * b)

            # 2. Dark outline: crisp deep blue-purple #1F1A3A
            if lum < 38 or (r <= 32 and g <= 28 and b <= 58 and lum < 50):
                polar.putpixel((x, y), (31, 26, 58, a))
                continue

            # 3. Feet & Legs (Y >= 98 with warm orange/red component)
            if y >= 98 and r > b:
                # Saturated vibrant polar orange feet
                fr = min(255, int(r * 1.15))
                fg = min(255, int(g * 1.1))
                fb = max(0, int(b * 0.85))
                polar.putpixel((x, y), (fr, fg, fb, a))
                continue

            # 4. Brass gold accents / rivets / ball joints
            is_brass = (r > 180 and g > 135 and b < 100)
            if is_brass:
                polar.putpixel((x, y), (r, g, b, a))
                continue

            # 5. Belly Plate area in bare chassis (high-lum area)
            if r > 180 and g > 180 and b > 180:
                # Pristine icy frost-white specular
                polar.putpixel((x, y), (248, 252, 255, a))
                continue

            # 6. Primary Body: Transform deep navy titanium to Brilliant Polar Frost Chrome
            # Navy lum typically ranges from 40 to 85
            f = max(0.0, min(1.0, (lum - 38) / 48.0))

            # Striking silver-white chrome ramp (#B8D2EB -> #DCEAF8 -> #F4FAFF)
            cr = int(140 + f * 110)  # 140..250
            cg = int(168 + f * 84)   # 168..252
            cb = int(195 + f * 60)   # 195..255

            if lum > 72:
                # Specular chrome glint
                cr = min(255, cr + 15)
                cg = min(255, cg + 10)
                cb = 255

            polar.putpixel((x, y), (cr, cg, cb, a))

    polar.save(out_path)
    print(f"✓ Created paint_polar_frost.png: {out_path}, bbox={polar.getbbox()}")
    return polar

def create_penguin_paint_ivory(src_path: str = "", out_path: str = "") -> Image.Image:
    if not src_path:
        src_path = f"{PENGUIN_DIR}/chassis/paint_penguin_navy.png"
    if not out_path:
        out_path = f"{PENGUIN_DIR}/chassis/paint_ivory_stock.png"

    navy = Image.open(src_path).convert("RGBA")
    w, h = navy.size
    ivory = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    for y in range(h):
        for x in range(w):
            px = cast(tuple[int, int, int, int], navy.getpixel((x, y)))
            r, g, b, a = px
            if a <= 10:
                continue

            # 1. Ground soft shadow at base
            if y >= 112 and (r < 50 and g < 50 and b < 80):
                ivory.putpixel((x, y), (r, g, b, a))
                continue

            lum = int(0.299 * r + 0.587 * g + 0.114 * b)

            # 2. Dark outline
            if lum < 38 or (r <= 32 and g <= 28 and b <= 58 and lum < 50):
                ivory.putpixel((x, y), (31, 26, 58, a))
                continue

            # 3. Feet & Legs
            if y >= 98 and r > b:
                ivory.putpixel((x, y), (r, g, b, a))
                continue

            # 4. Brass accents
            is_brass = (r > 180 and g > 135 and b < 100)
            if is_brass:
                ivory.putpixel((x, y), (r, g, b, a))
                continue

            # 5. Primary body to Warm Ivory Enamel (#E8DEC8 ~ #FDF8ED)
            f = max(0.0, min(1.0, (lum - 38) / 48.0))
            ir = int(210 + f * 43)   # 210..253
            ig = int(198 + f * 50)   # 198..248
            ib = int(178 + f * 58)   # 178..236

            ivory.putpixel((x, y), (ir, ig, ib, a))

    ivory.save(out_path)
    print(f"✓ Created paint_ivory_stock.png: {out_path}, bbox={ivory.getbbox()}")
    return ivory

if __name__ == "__main__":
    create_penguin_paint_polar_frost()
    create_penguin_paint_ivory()
