import os
from PIL import Image
from typing import cast

def measure_staff(img: Image.Image, xmin: int = 40, xmax: int = 120, ymin: int = 40, ymax: int = 120) -> tuple[float, int]:
    px = img.load()
    assert px is not None
    # Find cyan crystal / bronze staff points
    staff_pts = []
    for y in range(ymin, ymax):
        for x in range(xmin, xmax):
            p = cast(tuple[int, ...], px[x, y])
            if p[3] > 100:
                # staff wood/bronze or cyan crystal
                is_bronze = (120 <= p[0] <= 190 and 80 <= p[1] <= 150 and 30 <= p[2] <= 90)
                is_cyan = (p[1] > 160 and p[2] > 160 and p[0] < 120)
                if is_bronze:
                    staff_pts.append((x, y))
    return float(len(staff_pts)), len(staff_pts)

fb = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/fox_battle.png")
fi = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/party/fox_idle.png")
print("fox_battle bbox:", fb.getbbox())
