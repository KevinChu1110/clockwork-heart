#!/usr/bin/env python3
from PIL import Image
import numpy as np

m = Image.open("/tmp/masterpiece_hero_512.png").convert("RGBA")
arr = np.array(m)

# 完整戰錘提取：
# 鎚頭 (x: 55..185, y: 320..505)
# 握柄 (x: 175..365, y: 270..365)
weapon_layer = np.zeros_like(arr)
for y in range(265, 506):
    for x in range(55, 370):
        r, g, b, a = arr[y, x]
        if a > 20:
            is_hammer_head = (x <= 185 and y >= 320)
            is_shaft = (y >= 265 and y <= 365)
            is_ground = (y >= 480 and x <= 220)
            if is_hammer_head or is_shaft or is_ground:
                weapon_layer[y, x] = [r, g, b, a]

im_w = Image.fromarray(weapon_layer, mode="RGBA")
crop_w = im_w.crop((55, 265, 370, 506))
crop_w.save("/tmp/full_hammer_test.png")
print("Saved /tmp/full_hammer_test.png, size:", crop_w.size, "bbox:", crop_w.getbbox())
