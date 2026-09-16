#!/usr/bin/env python3
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

def build_char_tiger():
    src_p = "/tmp/tiger_standee_gen2.png"
    assert os.path.exists(src_p), f"Missing {src_p}"
    src = Image.open(src_p).convert("RGB")
    
    # Save high-res concept to docs/art/ember_tiger_concept.png
    concept_dst = "/opt/side/bravesoul-game/docs/art/ember_tiger_concept.png"
    src.save(concept_dst)
    print(f"✓ Saved high-res concept: {concept_dst}")

    # Studio background color matching char_rabbit.png and char_macaque.png
    # (235, 226, 209)
    BG_COLOR = (235, 226, 209)

    # Detect character bounds in src (928, 1152)
    # The background of src is (247, 238, 209)
    src_corner = cast(tuple[int, int, int], src.getpixel((0, 0)))
    print("Source corner color:", src_corner)

    w, h = src.size
    min_x, min_y, max_x, max_y = w, h, 0, 0
    # Create mask for character
    mask = Image.new("L", (w, h), 0)
    src_px = src.load()
    mask_px = mask.load()
    assert src_px is not None and mask_px is not None

    for y in range(h):
        for x in range(w):
            c = cast(tuple[int, int, int], src_px[x, y])
            diff = max(abs(c[0] - src_corner[0]), abs(c[1] - src_corner[1]), abs(c[2] - src_corner[2]))
            if diff > 18:
                mask_px[x, y] = 255
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)

    print(f"Detected character box: ({min_x}, {min_y}, {max_x}, {max_y}) size: {max_x - min_x}x{max_y - min_y}")

    # Crop with generous padding
    pad = 30
    crop_box = (max(0, min_x - pad), max(0, min_y - pad), min(w, max_x + pad), min(h, max_y + pad))
    cropped = src.crop(crop_box)
    
    # Target standee canvas: 400 x 840
    # We want character height to be around 640px, ground baseline around y=790..800
    char_h = max_y - min_y
    char_w = max_x - min_x
    target_char_h = 635
    scale = target_char_h / char_h
    new_w = int(round(cropped.width * scale))
    new_h = int(round(cropped.height * scale))
    
    scaled_crop = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Create 400x840 canvas
    standee = Image.new("RGB", (400, 840), BG_COLOR)
    
    # Position character:
    # Character center X should be 200
    # Character feet ground Y should be ~795
    char_top_offset = (min_y - crop_box[1]) * scale
    char_bottom_offset = (max_y - crop_box[1]) * scale
    char_center_offset = ((min_x + max_x) / 2 - crop_box[0]) * scale
    
    paste_x = int(round(200 - char_center_offset))
    paste_y = int(round(795 - char_bottom_offset))
    
    # Alpha blend or seamless paste:
    # Build RGBA of scaled_crop with feathered background
    rgba_crop = scaled_crop.convert("RGBA")
    rgba_px = rgba_crop.load()
    assert rgba_px is not None
    
    for y in range(new_h):
        for x in range(new_w):
            c = cast(tuple[int, int, int, int], rgba_px[x, y])
            diff = max(abs(c[0] - src_corner[0]), abs(c[1] - src_corner[1]), abs(c[2] - src_corner[2]))
            if diff < 14:
                rgba_px[x, y] = (c[0], c[1], c[2], 0)
            elif diff < 28:
                a = int(255 * (diff - 14) / 14.0)
                rgba_px[x, y] = (c[0], c[1], c[2], a)

    # First add a clean soft contact drop shadow per paperdoll_slots.json:
    # center: x: 200, y: 802, radius_x: 105, radius_y: 22, color: rgba(31, 26, 58, 0.35)
    shadow_img = Image.new("RGBA", (400, 840), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_img)
    s_draw.ellipse((200 - 105, 802 - 20, 200 + 105, 802 + 20), fill=(31, 26, 58, 90))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=8))

    # Composite onto canvas
    standee_rgba = Image.new("RGBA", (400, 840), BG_COLOR + (255,))
    standee_rgba.alpha_composite(shadow_img)
    standee_rgba.alpha_composite(rgba_crop, (paste_x, paste_y))

    final_standee = standee_rgba.convert("RGB")
    
    dst1 = "/opt/side/bravesoul-game/branding/char_tiger.png"
    dst2 = "/opt/side/bravesoul-game/web/media/hero/char_tiger.png"
    dst3 = "/opt/side/bravesoul-game/docs/art/char_tiger_candidate_400x840.png"
    
    final_standee.save(dst1)
    final_standee.save(dst2)
    final_standee.save(dst3)
    print(f"✓ Saved {dst1}")
    print(f"✓ Saved {dst2}")
    print(f"✓ Saved {dst3}")

if __name__ == "__main__":
    build_char_tiger()
