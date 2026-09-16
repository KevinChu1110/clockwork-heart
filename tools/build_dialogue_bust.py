#!/usr/bin/env python3
"""
tools/build_dialogue_bust.py
通用對話半身像去背與格式化工具：
- 讀取高解析度立繪概念圖，基於邊角純色背景執行漸層 Alpha 去背
- 導出標準規格 384x480 RGBA 對話框立繪圖片資產
"""
import os
from typing import cast
from PIL import Image

def build_dialogue_bust():
    src_p = "/opt/side/bravesoul-game/docs/art/ember_tiger_concept.png"
    src = Image.open(src_p).convert("RGB")
    src_corner = cast(tuple[int, int, int], src.getpixel((0, 0)))
    
    w, h = src.size
    rgba = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    src_px = src.load()
    rgba_px = rgba.load()
    assert src_px is not None and rgba_px is not None
    
    for y in range(h):
        for x in range(w):
            c = cast(tuple[int, int, int], src_px[x, y])
            diff = max(abs(c[0] - src_corner[0]), abs(c[1] - src_corner[1]), abs(c[2] - src_corner[2]))
            if diff < 16:
                continue
            elif diff < 28:
                a = int(255 * (diff - 16) / 12.0)
                rgba_px[x, y] = (c[0], c[1], c[2], a)
            else:
                rgba_px[x, y] = (c[0], c[1], c[2], 255)

    # Waist-up dialogue bust crop:
    # Top of head y=95 down to belt/waist y=770 (height=675)
    # Width: from winding key edge x=135 to right blade/shoulder x=785 (width=650)
    bust_crop_box = (135, 95, 785, 770)
    bust_cropped = rgba.crop(bust_crop_box)
    
    # Mask out any lower tail artifact below waist on far left (x < 70, y > 500 in cropped)
    bc_px = bust_cropped.load()
    assert bc_px is not None
    for cy in range(500, bust_cropped.height):
        for cx in range(80):
            bc_px[cx, cy] = (0, 0, 0, 0)
            
    # Scale to fill 384x480 comfortably: target height ~425px
    scale_bust = 425.0 / bust_cropped.height
    bw = int(round(bust_cropped.width * scale_bust))
    bh = int(round(bust_cropped.height * scale_bust))
    if bw > 368:
        scale_bust = 368.0 / bust_cropped.width
        bw = int(round(bust_cropped.width * scale_bust))
        bh = int(round(bust_cropped.height * scale_bust))
        
    scaled_bust = bust_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
    
    dialogue_bust = Image.new("RGBA", (384, 480), (0, 0, 0, 0))
    paste_x = (384 - bw) // 2
    paste_y = 480 - bh
    dialogue_bust.alpha_composite(scaled_bust, (paste_x, paste_y))
    
    dst_bust = "/opt/side/bravesoul-game/game/assets/sprites/portraits/ember_tiger.png"
    dialogue_bust.save(dst_bust)
    print(f"✓ Saved updated dialogue bust: {dst_bust} ({dialogue_bust.size}, bbox={dialogue_bust.getbbox()})")

if __name__ == "__main__":
    build_dialogue_bust()
