#!/usr/bin/env python3
import numpy as np
from PIL import Image

def test_shadow_removal():
    im = Image.open("/tmp/tortoise_lower_body.png").convert("RGBA")
    arr = np.array(im, dtype=np.float32)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    
    # Brightness
    brightness = (r + g + b) / 3.0
    # Saturation spread
    spread = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
    
    # 1. Pure white background
    is_white = (r > 240) & (g > 240) & (b > 240)
    
    # 2. Ground shadow: low saturation (spread < 45) and high brightness (brightness > 130)
    # in the bottom half of the image (y > 100 out of 165)
    y_idx = np.arange(arr.shape[0])[:, None]
    is_ground_shadow = (y_idx > 105) & (spread < 40) & (brightness > 120)
    
    # Faint shadow edge
    is_faint = (y_idx > 95) & (spread < 30) & (brightness > 140)
    
    mask = is_white | is_ground_shadow | is_faint
    arr[mask, 3] = 0
    
    res = Image.fromarray(arr.astype(np.uint8))
    res.save("/tmp/tortoise_lower_cleaned.png")
    
    # Test on magenta
    mag = Image.new("RGBA", res.size, (255, 0, 255, 255))
    mag.alpha_composite(res)
    mag.save("/tmp/tortoise_lower_magenta.png")
    print("Saved /tmp/tortoise_lower_magenta.png")

if __name__ == "__main__":
    test_shadow_removal()
