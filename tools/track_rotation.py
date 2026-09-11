#!/usr/bin/env python3
import sys
import os
import math
from typing import cast
from PIL import Image

def track_rotation():
    # deg = -65, target_hand = (84, 58)
    # rotation center in large_canvas is (128, 128)
    # paste offset was (128 - 93, 128 - 88) = (35, 40)
    # out_128 paste offset is (hx - 128, hy - 128) = (84 - 128, 58 - 128) = (-44, -70)
    
    # So a point (sx, sy) in clean_staff:
    # in large_canvas: (lx, ly) = (sx + 35, sy + 40)
    # rotated by -65 deg around (128, 128):
    # in PIL, rotate(deg) rotates counter-clockwise by deg.
    # deg = -65 means clockwise by 65 degrees!
    rad = math.radians(-65)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    # check points:
    # crystal: (95, 52)
    # grip: (93, 88)
    # bottom: (90, 120)
    for name, (sx, sy) in [("crystal", (95, 52)), ("grip", (93, 88)), ("bottom", (90, 120))]:
        lx = (sx - 93) * 0.98 + 128
        ly = (sy - 88) * 0.98 + 128
        # rotate counter-clockwise by -65 deg around 128, 128
        rx = 128 + cos_a * (lx - 128) - sin_a * (ly - 128)
        ry = 128 + sin_a * (lx - 128) + cos_a * (ly - 128)
        # paste to out_128 at (hx - 128, hy - 128) = (84 - 128, 58 - 128)
        fx = rx - 128 + 84
        fy = ry - 128 + 58
        print(f"{name} ({sx},{sy}) -> out_128 at approx ({fx:.1f}, {fy:.1f})")

if __name__ == "__main__":
    track_rotation()
