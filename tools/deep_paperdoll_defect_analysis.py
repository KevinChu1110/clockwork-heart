import os
import json
import numpy as np
from PIL import Image
from collections import Counter

races = ["lion", "fox", "boar", "macaque", "tiger", "crane", "bear", "penguin"]
base_paperdoll = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll"

def get_brightness(rgb):
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]

def get_dominant_color(img_path, ignore_dark=True):
    if not os.path.exists(img_path):
        return None, 0
    im = Image.open(img_path).convert("RGBA")
    arr = np.array(im)
    mask = arr[:, :, 3] > 200
    pixels = arr[mask][:, :3]
    if len(pixels) == 0:
        return None, 0
    if ignore_dark:
        # ignore dark borders (R,G,B all < 60)
        valid = ~((pixels[:, 0] < 60) & (pixels[:, 1] < 60) & (pixels[:, 2] < 60))
        if np.sum(valid) > 0:
            pixels = pixels[valid]
    # count unique
    colors, counts = np.unique(pixels, axis=0, return_counts=True)
    top_idx = np.argmax(counts)
    return tuple(int(x) for x in colors[top_idx]), len(pixels)

print("="*80)
print("DEFECT 3 AUDIT: Head / Ear color vs Chassis color across paints")
print("="*80)

for r in races:
    print(f"\n--- RACE: {r} ---")
    r_dir = os.path.join(base_paperdoll, r)
    head_dir = os.path.join(r_dir, "head_unit")
    chassis_dir = os.path.join(r_dir, "chassis")
    
    head_files = [f for f in os.listdir(head_dir) if f.endswith("_512.png")] if os.path.exists(head_dir) else []
    chassis_files = [f for f in os.listdir(chassis_dir) if f.endswith("_512.png")] if os.path.exists(chassis_dir) else []
    
    print(f"  Head files: {head_files}")
    print(f"  Chassis files: {chassis_files}")
    
    for hf in head_files:
        hp = os.path.join(head_dir, hf)
        h_col, h_cnt = get_dominant_color(hp)
        h_bright = get_brightness(h_col) if h_col else 0
        print(f"  HEAD [{hf}]: top RGB={h_col}, brightness={h_bright:.1f}, count={h_cnt}")
    
    for cf in chassis_files:
        cp = os.path.join(chassis_dir, cf)
        c_col, c_cnt = get_dominant_color(cp)
        c_bright = get_brightness(c_col) if c_col else 0
        print(f"  CHASSIS [{cf}]: top RGB={c_col}, brightness={c_bright:.1f}, count={c_cnt}")
        
        # compare with head files
        for hf in head_files:
            hp = os.path.join(head_dir, hf)
            h_col, _ = get_dominant_color(hp)
            if h_col and c_col:
                delta_b = abs(get_brightness(h_col) - get_brightness(c_col))
                rgb_dist = np.linalg.norm(np.array(h_col) - np.array(c_col))
                print(f"    vs Head [{hf}]: RGB dist={rgb_dist:.1f}, Brightness delta={delta_b:.1f}")

print("\n" + "="*80)
print("DEFECT 1 & 2 AUDIT: Costume thickness and Neckline analysis")
print("="*80)

for r in races:
    print(f"\n--- RACE: {r} ---")
    costume_dir = os.path.join(base_paperdoll, r, "costume")
    if not os.path.exists(costume_dir):
        print("  Costume dir not found")
        continue
    c_files = sorted([f for f in os.listdir(costume_dir) if f.endswith("_512.png")])
    for cf in c_files:
        cp = os.path.join(costume_dir, cf)
        im = Image.open(cp).convert("RGBA")
        arr = np.array(im)
        alpha = arr[:, :, 3]
        opaque_px = np.sum(alpha > 128)
        bbox = im.split()[3].getbbox()
        
        # Neckline straight horizontal line analysis:
        # Find the top-most opaque pixels in the center neck/chest region (x between 200 and 312)
        center_alpha = alpha[:, 200:312]
        top_y_per_col = []
        for col_idx in range(center_alpha.shape[1]):
            col = center_alpha[:, col_idx]
            opaque_indices = np.where(col > 128)[0]
            if len(opaque_indices) > 0:
                top_y_per_col.append(opaque_indices[0])
        
        y_variance = np.var(top_y_per_col) if len(top_y_per_col) > 5 else 0
        y_min = np.min(top_y_per_col) if len(top_y_per_col) > 0 else 0
        y_max = np.max(top_y_per_col) if len(top_y_per_col) > 0 else 0
        y_range = y_max - y_min
        
        # Check if top row is flat:
        is_flat_horizontal = (y_range <= 1 and len(top_y_per_col) > 20)
        
        print(f"  Costume [{cf}]:")
        print(f"    Opaque pixels: {opaque_px}, bbox: {bbox}")
        print(f"    Center neckline Y: min={y_min}, max={y_max}, span={y_range}, var={y_variance:.2f}")
        print(f"    Strict flat top edge: {is_flat_horizontal}")
