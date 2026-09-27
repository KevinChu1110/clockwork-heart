from typing import cast
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/wolf"
chassis_128 = Image.open(f"{PD_DIR}/chassis/chassis_wolf_warm_orange_default.png").convert("RGBA")

w, h = 128, 128
leg_l = Image.new("RGBA", (w, h), (0, 0, 0, 0))
leg_r = Image.new("RGBA", (w, h), (0, 0, 0, 0))
pelvis = Image.new("RGBA", (w, h), (0, 0, 0, 0))
torso_chassis = Image.new("RGBA", (w, h), (0, 0, 0, 0))

ch_px = chassis_128.load()
assert ch_px is not None

for y in range(h):
    for x in range(w):
        p = cast(tuple[int, int, int, int], ch_px[x, y])
        if p[3] == 0:
            continue
        if y >= 117:
            continue
        if y < 96:
            torso_chassis.putpixel((x, y), p)
        if 88 <= y <= 104:
            pelvis.putpixel((x, y), p)
        if 90 <= y <= 116:
            if x <= 58:
                leg_l.putpixel((x, y), p)
            elif x >= 60:
                leg_r.putpixel((x, y), p)

print("Torso chassis bbox:", torso_chassis.getbbox())
print("Pelvis bbox:", pelvis.getbbox())
print("Leg L bbox:", leg_l.getbbox())
print("Leg R bbox:", leg_r.getbbox())
