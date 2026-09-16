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

    # Studio background color matching char_rabbit.png and char_macaque.png: (235, 226, 209)
    BG_COLOR = (235, 226, 209)
    src_corner = cast(tuple[int, int, int], src.getpixel((0, 0)))
    print("Source corner color:", src_corner)

    w, h = src.size
    min_x, min_y, max_x, max_y = 85, 102, 869, 1113
    print(f"Detected character box: ({min_x}, {min_y}, {max_x}, {max_y}) size: {max_x - min_x + 1}x{max_y - min_y + 1}")

    # Crop with minimal padding to preserve exact bounding box
    pad = 6
    crop_box = (max(0, min_x - pad), max(0, min_y - pad), min(w, max_x + pad), min(h, max_y + pad))
    cropped = src.crop(crop_box)
    
    char_w = max_x - min_x + 1
    char_h = max_y - min_y + 1

    # Target standee canvas: 400 x 840
    # To satisfy Rule 16 / 4c-5 and ensure both blades are fully visible with margins >= 8px on left and right:
    # We set target_w = 376px, leaving ~24px total horizontal margin (12px left, 12px right).
    target_w = 376
    scale = target_w / char_w
    new_w = int(round(cropped.width * scale))
    new_h = int(round(cropped.height * scale))
    
    scaled_crop = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Build RGBA of scaled_crop with feathered background removal
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

    # Find actual non-zero alpha bounding box of the character
    alpha_box = rgba_crop.getbbox()
    assert alpha_box is not None
    actual_w = alpha_box[2] - alpha_box[0]
    total_margin_x = 400 - actual_w
    left_margin = total_margin_x // 2
    paste_x = left_margin - alpha_box[0]

    # Feet ground baseline: in src, feet touch around y=1085
    feet_crop_y = (1085 - crop_box[1]) * scale
    target_ground_y = 790
    paste_y = int(round(target_ground_y - feet_crop_y))

    # Contact ground shadow
    shadow_img = Image.new("RGBA", (400, 840), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_img)
    s_draw.ellipse((200 - 100, target_ground_y - 15, 200 + 100, target_ground_y + 15), fill=(31, 26, 58, 85))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=7))

    # Composite onto canvas
    standee_rgba = Image.new("RGBA", (400, 840), BG_COLOR + (255,))
    standee_rgba.alpha_composite(shadow_img)
    standee_rgba.alpha_composite(rgba_crop, (paste_x, paste_y))

    final_standee = standee_rgba.convert("RGB")
    
    # Verify margins and non-bg pixels at boundaries
    final_arr = np.array(final_standee)
    diff_bg = np.max(np.abs(final_arr.astype(int) - np.array(BG_COLOR).astype(int)), axis=2)
    col_399_non_bg = np.sum(diff_bg[:, 399] > 15)
    row_0_non_bg = np.sum(diff_bg[0, :] > 15)
    char_mask = diff_bg > 15
    c_ys, c_xs = np.where(char_mask)
    left_margin_actual = int(c_xs.min())
    right_margin_actual = int(399 - c_xs.max())
    print(f"Non-bg pixels: Col 399 = {col_399_non_bg}, Row 0 = {row_0_non_bg}")
    print(f"Margins: Left = {left_margin_actual}px, Right = {right_margin_actual}px")
    assert col_399_non_bg == 0, f"Right column has non-bg pixels: {col_399_non_bg}"
    assert row_0_non_bg == 0, f"Top row has non-bg pixels: {row_0_non_bg}"
    assert left_margin_actual >= 8, f"Left margin too small: {left_margin_actual}"
    assert right_margin_actual >= 8, f"Right margin too small: {right_margin_actual}"

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
