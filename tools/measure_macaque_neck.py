#!/usr/bin/env python3
from PIL import Image

MACAQUE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque"

im_ch = Image.open(f"{MACAQUE_DIR}/chassis/paint_ivory_stock_512.png").convert("RGBA")
im_hd = Image.open(f"{MACAQUE_DIR}/head_unit/ear_macaque_coaxial_512.png").convert("RGBA")

# 檢查 Y=250..270 的軀幹 X 範圍
for y in [240, 250, 255, 260, 265, 270]:
    xs_ch = [x for x in range(512) if im_ch.getpixel((x, y))[3] > 100]
    xs_hd = [x for x in range(512) if im_hd.getpixel((x, y))[3] > 100]
    ch_c = (min(xs_ch) + max(xs_ch))/2.0 if xs_ch else 0
    hd_c = (min(xs_hd) + max(xs_hd))/2.0 if xs_hd else 0
    print(f"Y={y}: chassis X center={ch_c:.1f} (range {min(xs_ch) if xs_ch else 0}..{max(xs_ch) if xs_ch else 0}), head X center={hd_c:.1f} (range {min(xs_hd) if xs_hd else 0}..{max(xs_hd) if xs_hd else 0})")
