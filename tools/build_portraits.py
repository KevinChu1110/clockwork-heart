#!/usr/bin/env python3
import os
from typing import cast
from PIL import Image

def build_portraits():
    src_p = "/opt/side/bravesoul-game/docs/art/ember_tiger_concept.png"
    assert os.path.exists(src_p), f"Missing {src_p}"
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
                
    # 2. Dialogue bust portrait: ember_tiger.png (384 x 480 RGBA)
    # Include winding key (x from 130), head top (y from 95), down to mid-torso/waist (y up to 660)
    # Right side: includes right shoulder and blade handle (up to x=790)
    # Crop box: (130, 95, 790, 665) -> width=660, height=570
    bust_crop_box = (130, 95, 790, 665)
    bust_cropped = rgba.crop(bust_crop_box)
    
    # Clean any stray pixels on the far lower-left that belong to lower tail:
    # In bust_cropped coordinates: x < 80 and y > 450 (which was x < 210, y > 545 in src)
    bc_px = bust_cropped.load()
    assert bc_px is not None
    for cy in range(430, bust_cropped.height):
        for cx in range(90):
            bc_px[cx, cy] = (0, 0, 0, 0)
    
    # Scale bust so height is ~430px (leaving ~50px headroom at top)
    target_h = 425
    scale_bust = target_h / bust_cropped.height
    bw = int(round(bust_cropped.width * scale_bust))
    bh = int(round(bust_cropped.height * scale_bust))
    if bw > 368:
        scale_bust = 368.0 / bust_cropped.width
        bw = int(round(bust_cropped.width * scale_bust))
        bh = int(round(bust_cropped.height * scale_bust))
        
    scaled_bust = bust_cropped.resize((bw, bh), Image.Resampling.LANCZOS)
    
    dialogue_bust = Image.new("RGBA", (384, 480), (0, 0, 0, 0))
    paste_x = (384 - bw) // 2
    paste_y = 480 - bh  # bottom aligned
    dialogue_bust.alpha_composite(scaled_bust, (paste_x, paste_y))
    
    dst_bust = "/opt/side/bravesoul-game/game/assets/sprites/portraits/ember_tiger.png"
    dialogue_bust.save(dst_bust)
    print(f"✓ Saved dialogue bust: {dst_bust} ({dialogue_bust.size}, bbox={dialogue_bust.getbbox()})")

    # 3. HUD combat portrait: tiger.png (128 x 128 RGBA)
    # Tight head-and-shoulders crop centered on head: x=230..730, y=95..525
    hud_crop_box = (230, 95, 730, 525)
    hud_cropped = rgba.crop(hud_crop_box)
    
    target_hud_dim = 100
    scale_hud = target_hud_dim / max(hud_cropped.width, hud_cropped.height)
    hw = int(round(hud_cropped.width * scale_hud))
    hh = int(round(hud_cropped.height * scale_hud))
    scaled_hud = hud_cropped.resize((hw, hh), Image.Resampling.LANCZOS)
    
    hud_portrait = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    paste_hud_x = (128 - hw) // 2
    paste_hud_y = (128 - hh) // 2
    hud_portrait.alpha_composite(scaled_hud, (paste_hud_x, paste_hud_y))
    
    dst_hud = "/opt/side/bravesoul-game/game/assets/sprites/portraits/tiger.png"
    hud_portrait.save(dst_hud)
    print(f"✓ Saved HUD portrait: {dst_hud} ({hud_portrait.size}, bbox={hud_portrait.getbbox()})")

if __name__ == "__main__":
    build_portraits()
