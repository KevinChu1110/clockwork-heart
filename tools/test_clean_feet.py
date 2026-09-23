#!/usr/bin/env python3
import numpy as np
from PIL import Image

def clean_ground():
    im = Image.open("/tmp/xuanji_tortoise_concept.png").convert("RGBA")
    arr = np.array(im)
    
    # Analyze pixels at y >= 680
    r = arr[:, :, 0].astype(int)
    g = arr[:, :, 1].astype(int)
    b = arr[:, :, 2].astype(int)
    
    # Pure white background: r>240, g>240, b>240
    is_white_bg = (r > 240) & (g > 240) & (b > 240)
    
    # Ground shadow / light floor:
    # Floor shadow appears at y >= 670 where colors are light beige/grayish/faint brown
    # Character feet/claws are dark: r < 130, g < 130, b < 130 or strongly saturated jade green (g > r + 30)
    # So ground shadow is: y >= 670 and (r > 135) and (g > 125) and (b > 110)
    is_ground_shadow = (np.arange(arr.shape[0])[:, None] >= 670) & (r > 135) & (g > 125) & (b > 110)
    
    # Also clean shadow between y >= 695 where r > 115, g > 105, b > 95
    is_deep_ground = (np.arange(arr.shape[0])[:, None] >= 695) & (r > 115) & (g > 105) & (b > 95)
    
    bg_mask = is_white_bg | is_ground_shadow | is_deep_ground
    
    # Set alpha
    arr[bg_mask, 3] = 0
    
    cleaned_im = Image.fromarray(arr)
    bbox = cleaned_im.getbbox()
    print("Cleaned bbox:", bbox)
    cropped = cleaned_im.crop(bbox)
    
    # Scale to 128x128
    target_h = 82
    scale = target_h / cropped.height
    target_w = int(cropped.width * scale)
    scaled = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    px = 64 - target_w // 2
    py = 114 - target_h
    canvas.paste(scaled, (px, py), scaled)
    
    # Magenta test
    mag = Image.new("RGBA", (128, 128), (255, 0, 255, 255))
    mag.alpha_composite(canvas)
    mag.save("/tmp/tortoise_feet_clean_magenta.png")
    canvas.save("/tmp/tortoise_master_perfect.png")
    print("Saved /tmp/tortoise_feet_clean_magenta.png")

if __name__ == "__main__":
    clean_ground()
