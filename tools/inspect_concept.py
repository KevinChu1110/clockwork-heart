#!/usr/bin/env python3
import numpy as np
from PIL import Image

def main():
    im = Image.open("/tmp/xuanji_tortoise_concept.png").convert("RGBA")
    w, h = im.size
    print(f"Loaded concept image: {w}x{h}")
    
    # Check background color around corners
    corners = [im.getpixel((5, 5)), im.getpixel((w-5, 5)), im.getpixel((5, h-5)), im.getpixel((w-5, h-5))]
    print("Corners RGB:", corners)
    
    # Remove white background
    data = np.array(im)
    r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
    
    # Background is near white (e.g. r>240, g>240, b>240)
    bg_mask = (r > 240) & (g > 240) & (b > 240)
    
    # Non-bg bounding box
    non_bg_y, non_bg_x = np.where(~bg_mask)
    if len(non_bg_x) > 0:
        min_x, max_x = int(np.min(non_bg_x)), int(np.max(non_bg_x))
        min_y, max_y = int(np.min(non_bg_y)), int(np.max(non_bg_y))
        print(f"Character bounding box: x=[{min_x}, {max_x}] (w={max_x - min_x + 1}), y=[{min_y}, {max_y}] (h={max_y - min_y + 1})")
    else:
        print("No foreground found!")

if __name__ == "__main__":
    main()
