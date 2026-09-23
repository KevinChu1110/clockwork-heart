#!/usr/bin/env python3
import numpy as np
from PIL import Image, ImageFilter

def extract_character():
    im = Image.open("/tmp/xuanji_tortoise_concept.png").convert("RGBA")
    w, h = im.size
    
    # Background removal using color distance and connectivity
    arr = np.array(im, dtype=np.float32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    
    # Near-white or very light gray floor
    # Ground shadow has min RGB > 140 and max(r,g,b)-min(r,g,b) < 30
    is_white_bg = (r > 240) & (g > 240) & (b > 240)
    # Ground faint shadow below feet (y > 700)
    is_floor_shadow = np.zeros_like(is_white_bg)
    is_floor_shadow[702:, :] = (r[702:, :] > 150) & (g[702:, :] > 140) & (b[702:, :] > 130)
    
    bg_mask = is_white_bg | is_floor_shadow
    
    # Smooth alpha
    alpha = np.where(bg_mask, 0, 255).astype(np.uint8)
    alpha_im = Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(0.8))
    
    im.putalpha(alpha_im)
    
    # Crop to character bbox
    bbox = im.getbbox()
    print("Cleaned bbox:", bbox)
    cropped = im.crop(bbox)
    
    # Fit into 128x128
    # Target height 82px (so head y is around 32, feet y at 114, shadow at 116..122)
    target_h = 82
    scale = target_h / cropped.height
    target_w = int(cropped.width * scale)
    scaled = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    # Place feet at y=114, centered at x=64
    px = 64 - target_w // 2
    py = 114 - target_h
    canvas.paste(scaled, (px, py), scaled)
    
    canvas.save("/tmp/tortoise_master_clean.png")
    print(f"Saved /tmp/tortoise_master_clean.png, placed at ({px}, {py}), bbox:", canvas.getbbox())

    # Save magenta preview
    mag = Image.new("RGBA", (128, 128), (255, 0, 255, 255))
    mag.alpha_composite(canvas)
    mag.save("/tmp/tortoise_clean_magenta.png")
    print("Saved /tmp/tortoise_clean_magenta.png")

if __name__ == "__main__":
    extract_character()
