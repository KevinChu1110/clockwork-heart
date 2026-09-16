#!/usr/bin/env python3
"""
tools/build_bear_quarry_chassis.py
Constructs paint_iron_quarry.png (重裝礦山玄鐵灰烤漆) for The Iron Bear paperdoll chassis.
- Source: game/assets/sprites/player/paperdoll/bear/chassis/paint_bear_amber.png
- Archetype: 戰士 (Viking) 重型機甲素體
- Style: 沉穩冷淬礦山玄鐵灰琺瑯 (Quarry Iron Grey Enamel) with bright brass ball-joints.
- Pure clockwork toy aesthetic: zero fur, zero biological meat, crisp #1F1A3A outline.
- Fully compliant with review.md 0-ART9 (zero weapons on chassis, fists completely bare).
- 128x128 RGBA
"""

from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BEAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bear"

def create_bear_paint_iron_quarry(src_path: str = "", out_path: str = "") -> Image.Image:
    if not src_path:
        src_path = f"{BEAR_DIR}/chassis/paint_bear_amber.png"
    if not out_path:
        out_path = f"{BEAR_DIR}/chassis/paint_iron_quarry.png"

    amber = Image.open(src_path).convert("RGBA")
    w, h = amber.size
    quarry = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    for y in range(h):
        for x in range(w):
            px = cast(tuple[int, int, int, int], amber.getpixel((x, y)))
            r, g, b, a = px
            if a <= 10:
                continue

            # Ground soft shadow at base (Y >= 115)
            if y >= 115 and (r < 60 and g < 60 and b < 80):
                quarry.putpixel((x, y), (r, g, b, a))
                continue

            lum = int(0.299 * r + 0.587 * g + 0.114 * b)

            # 1. Dark outline: crisp deep blue-purple #1F1A3A
            if lum < 50 or (r <= 35 and g <= 30 and b <= 60):
                quarry.putpixel((x, y), (31, 26, 58, a))
                continue

            # 2. Check if pixel is brass gold accent / rivet / ball joint (high yellow/gold)
            is_brass = (r > 190 and g > 150 and b < 80)
            if is_brass:
                # Keep brilliant brass gold for dramatic cold-warm contrast
                quarry.putpixel((x, y), (r, g, b, a))
                continue

            # 3. Check if pixel is white plate (chest/belly plate, e.g. #FFF8E7)
            is_white_plate = (r > 230 and g > 220 and b > 200)
            if is_white_plate:
                # Cold polished titanium white-steel (#DCE6F5)
                f_w = (lum - 200) / 55.0
                wr = int(195 + f_w * 45)
                wg = int(210 + f_w * 40)
                wb = int(235 + f_w * 20)
                quarry.putpixel((x, y), (max(0, min(255, wr)), max(0, min(255, wg)), max(0, min(255, wb)), a))
                continue

            # 4. Dark steel joints / clamps
            is_dark_joint = (r < 90 and g < 100 and b < 120 and r < g + 15 and b >= r)
            if is_dark_joint:
                # Deep forged obsidian steel (#1E222D)
                quarry.putpixel((x, y), (30, 34, 46, a))
                continue

            # 5. Primary amber body (e.g. #D97724, r > g > b) -> Quarry Iron Steel (#384256 ~ #8EA0C0)
            f = max(0.0, min(1.0, (lum - 40) / 160.0))
            sr = int(36 + f * 98)   # 36..134
            sg = int(46 + f * 116)  # 46..162
            sb = int(68 + f * 148)  # 68..216

            # Specular edge on high-luminance steel curves
            if lum > 165:
                sr = min(230, sr + 45)
                sg = min(240, sg + 48)
                sb = min(255, sb + 40)

            quarry.putpixel((x, y), (sr, sg, sb, a))

    quarry.save(out_path)
    print(f"✓ Created paint_iron_quarry.png: {out_path}, bbox={quarry.getbbox()}")
    return quarry

if __name__ == "__main__":
    create_bear_paint_iron_quarry()
