import os
import numpy as np
from PIL import Image

def analyze(path, name):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return None
    im = Image.open(path).convert('RGBA')
    arr = np.array(im)
    alpha = arr[:, :, 3]
    bbox = im.split()[3].getbbox()
    
    # Check for flat horizontal line at top
    # For each column in bbox, find first y with alpha > 128
    top_y = []
    for x in range(bbox[0], bbox[2]):
        col = alpha[:, x]
        op = np.where(col > 128)[0]
        if len(op) > 0:
            top_y.append((x, int(op[0])))
    
    # Center neck/chest region: x between 200 and 312
    center_ys = [y for x, y in top_y if 200 <= x < 312]
    var = float(np.var(center_ys)) if len(center_ys) > 5 else 0.0
    y_min = int(np.min(center_ys)) if center_ys else 0
    y_max = int(np.max(center_ys)) if center_ys else 0
    
    print(f"=== {name} ===")
    print(f"bbox: {bbox}, center len: {len(center_ys)}, min_y={y_min}, max_y={y_max}, span={y_max-y_min}, var={var:.2f}")
    
    # Count how many contiguous pixels have the exact min_y in the center region
    flat_len = 0
    max_flat_len = 0
    cur_flat_len = 0
    prev_y = None
    for y in center_ys:
        if y == prev_y:
            cur_flat_len += 1
            if cur_flat_len > max_flat_len:
                max_flat_len = cur_flat_len
        else:
            cur_flat_len = 1
            prev_y = y
    print(f"Max contiguous flat pixels in center: {max_flat_len}")
    return top_y

analyze('/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/bear/costume/costume_berserker_cuirass_512.png', 'Bear Berserker')
analyze('/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/penguin/costume/costume_abyssal_diver_cuirass_512.png', 'Penguin Abyssal Diver')
analyze('/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tiger/costume/costume_ember_tunic_512.png', 'Tiger Ember Tunic')
analyze('/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/bear/costume/costume_ironclad_overalls_512.png', 'Bear Ironclad Overalls')
