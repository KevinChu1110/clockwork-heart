#!/usr/bin/env python3
import math
import numpy as np
from PIL import Image, ImageDraw

def draw_spring_tail():
    w, h = 76, 192
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    # 繪製彈簧長尾巴：從左上 (10, 108 附近) 接合臀部，向下優雅彎曲伸展
    # 彈簧節數：7 節螺旋圈
    # 顏色：
    # 描邊: #1F1A3A (31, 26, 58)
    # 金屬高光: #FFEAA0
    # 金屬主體: #FFD028 (黃銅) 與 #E0E8F0 (合金銀鋼)
    # 暗部陰影: #7A5810

    # 繪製連續的彈簧線圈
    # 頂部接合金屬基座軸承 (10, 104) 附近
    d.ellipse([4, 100, 22, 116], fill=(130, 95, 30, 255), outline=(31, 26, 58, 255), width=3)
    d.ellipse([7, 103, 19, 113], fill=(255, 208, 40, 255))

    # 彈簧環曲線
    rings = [
        (12, 92, 28, 20, 15),
        (18, 76, 32, 22, 20),
        (26, 58, 36, 24, 25),
        (35, 40, 36, 24, 20),
        (42, 22, 32, 22, 10),
        (46, 6, 28, 20, -10),
        (42, 0, 24, 18, -30),
        (34, 12, 22, 18, -60),
        (28, 28, 24, 20, -40),
        (26, 48, 26, 22, -10),
        (30, 68, 28, 22, 20),
        (36, 88, 30, 24, 30),
        (44, 108, 30, 24, 40),
        (50, 128, 26, 22, 50),
        (52, 146, 22, 20, 60),
        (48, 162, 18, 18, 70),
    ]

    # 繪製由上至下伸展的螺旋尾巴
    for rx, ry, rw, rh, ang in rings:
        # 後半環 (暗面)
        d.ellipse([rx, ry, rx + rw, ry + rh], outline=(31, 26, 58, 255), width=4)
        d.ellipse([rx + 2, ry + 2, rx + rw - 2, ry + rh - 2], fill=(200, 150, 30, 255))
        d.ellipse([rx + 4, ry + 4, rx + rw - 4, ry + rh - 4], fill=(255, 225, 120, 255))
        d.ellipse([rx + 7, ry + 7, rx + rw - 7, ry + rh - 7], fill=(0, 0, 0, 0))

    # 末端小金屬發條小銅珠 (42, 172)
    d.ellipse([42, 172, 56, 186], fill=(255, 208, 40, 255), outline=(31, 26, 58, 255), width=3)
    d.ellipse([45, 175, 49, 179], fill=(255, 255, 255, 255))

    im.save("/tmp/macaque_test/spring_tail_test.png")
    print("Saved /tmp/macaque_test/spring_tail_test.png, size:", im.size, "bbox:", im.getbbox())

draw_spring_tail()
