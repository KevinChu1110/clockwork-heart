#!/usr/bin/env python3
import os
from typing import cast
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/tortoise"
chassis_128 = Image.open(f"{PD_DIR}/chassis/paint_tortoise_jade.png").convert("RGBA")
ch_px = chassis_128.load()
assert ch_px is not None

w, h = 128, 128

leg_l = Image.new("RGBA", (w, h), (0, 0, 0, 0))
leg_r = Image.new("RGBA", (w, h), (0, 0, 0, 0))
torso_chassis = Image.new("RGBA", (w, h), (0, 0, 0, 0))

for y in range(h):
    for x in range(w):
        p = cast(tuple[int, int, int, int], ch_px[x, y])
        if p[3] == 0:
            continue
        # Pure soft shadow
        if p[3] < 150 and p[0] < 35 and p[1] < 30 and p[2] < 65:
            continue
        # Torso includes body and lower rim up to y=102
        if y < 102:
            torso_chassis.putpixel((x, y), p)
        # Legs include hip socket connection from y=90 downward
        if y >= 90:
            if x <= 58:
                leg_l.putpixel((x, y), p)
            elif x >= 64:
                leg_r.putpixel((x, y), p)
            elif y >= 102:
                torso_chassis.putpixel((x, y), p)

print("Torso bbox:", torso_chassis.getbbox())
print("Leg L bbox:", leg_l.getbbox())
print("Leg R bbox:", leg_r.getbbox())
