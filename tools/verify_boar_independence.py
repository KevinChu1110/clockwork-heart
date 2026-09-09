#!/usr/bin/env python3
from PIL import Image

boar_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar"
costume = Image.open(f"{boar_dir}/costume/costume_viking_ironclad.png").convert("RGBA")

chassis_list = ["paint_brass_gold.png", "paint_ivory_stock.png", "paint_molten_crimson.png"]

for ch_name in chassis_list:
    ch = Image.open(f"{boar_dir}/chassis/{ch_name}").convert("RGBA")
    total_costume_opaque = 0
    overlap = 0
    same_color = 0
    for y in range(128):
        for x in range(128):
            cp = costume.getpixel((x, y))
            chp = ch.getpixel((x, y))
            if cp[3] > 0:
                total_costume_opaque += 1
                if chp[3] > 0:
                    overlap += 1
                    if cp[:3] == chp[:3]:
                        same_color += 1
    same_ratio = (same_color / total_costume_opaque) * 100.0 if total_costume_opaque else 0.0
    print(f"Chassis {ch_name:25}: Overlap = {overlap} px, Same Color = {same_color} px ({same_ratio:.2f}%)")
