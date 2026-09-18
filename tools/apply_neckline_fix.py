import os
import math
import numpy as np
from PIL import Image

REPO_ROOT = '/opt/side/bravesoul-game'

def warp_neckline_collar(im, x_range, y_top_orig, max_offset, y_fade_end):
    w, h = im.size
    assert w == 512 and h == 512
    arr = np.array(im, dtype=np.float32)
    new_arr = arr.copy()
    
    x_min, x_max = x_range
    x_center = (x_min + x_max) / 2.0
    x_half = (x_max - x_min) / 2.0
    
    for x in range(w):
        if x < x_min or x > x_max:
            continue
        
        nx = (x - x_center) / x_half
        curve_factor = 0.5 * (1.0 + math.cos(math.pi * nx))
        col_offset = max_offset * curve_factor
        
        if col_offset <= 0:
            continue
            
        for y in range(int(y_top_orig - 5), int(y_fade_end + 10)):
            if y < 0 or y >= h:
                continue
            
            if y < y_top_orig:
                fade = 1.0
            elif y >= y_fade_end:
                fade = 0.0
            else:
                t = (y - y_top_orig) / (y_fade_end - y_top_orig)
                fade = (1.0 - t) ** 1.3
            
            shift = col_offset * fade
            y_src = y - shift
            
            if y_src < 0:
                new_arr[y, x] = [0, 0, 0, 0]
            else:
                y0 = int(math.floor(y_src))
                y1 = min(h - 1, y0 + 1)
                fy = y_src - y0
                new_arr[y, x] = (1.0 - fy) * arr[y0, x] + fy * arr[y1, x]
    
    return Image.fromarray(np.clip(new_arr, 0, 255).astype(np.uint8), mode='RGBA')

def main():
    bear_path = os.path.join(REPO_ROOT, 'game/assets/sprites/player/paperdoll/bear/costume/costume_berserker_cuirass_512.png')
    pen_path = os.path.join(REPO_ROOT, 'game/assets/sprites/player/paperdoll/penguin/costume/costume_abyssal_diver_cuirass_512.png')
    
    # Save original backups in proofs/neckline_fix/backups/
    os.makedirs('proofs/neckline_fix/backups', exist_ok=True)
    bear_im = Image.open(bear_path).convert('RGBA')
    pen_im = Image.open(pen_path).convert('RGBA')
    
    bear_im.save('proofs/neckline_fix/backups/costume_berserker_cuirass_512_orig.png')
    pen_im.save('proofs/neckline_fix/backups/costume_abyssal_diver_cuirass_512_orig.png')
    
    # Apply warp
    bear_fixed = warp_neckline_collar(bear_im, x_range=(192, 320), y_top_orig=216, max_offset=8.0, y_fade_end=242)
    pen_fixed = warp_neckline_collar(pen_im, x_range=(190, 322), y_top_orig=192, max_offset=8.0, y_fade_end=218)
    
    # Save to actual game asset paths
    bear_fixed.save(bear_path, optimize=True)
    pen_fixed.save(pen_path, optimize=True)
    print("Successfully applied neckline fix to both costume PNGs!")

if __name__ == '__main__':
    main()
