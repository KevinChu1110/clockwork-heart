#!/usr/bin/env python3
from typing import cast
from PIL import Image

chassis = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png").convert("RGBA")
head = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/head_unit/ear_macaque_coaxial.png").convert("RGBA")
tunic = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/costume/costume_dawn_monk_tunic.png").convert("RGBA")

bare = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
bare = Image.alpha_composite(bare, chassis)
bare = Image.alpha_composite(bare, head)

print("Tunic vs bare in center (x=48..65):")
for y in range(58, 66):
    s = f"y={y:2d}: "
    for x in range(48, 66):
        ta = cast(tuple[int,int,int,int], tunic.getpixel((x, y)))[3]
        br, bg, bb, ba = cast(tuple[int,int,int,int], bare.getpixel((x, y)))
        is_dark = (ba > 150 and br < 110 and bg < 90 and bb < 80)
        s += f"[{'T' if ta>30 else '.'}{'D' if is_dark else '.'}] "
    print(s)
