import os
import numpy as np
from PIL import Image

races = ['fox', 'lion', 'boar', 'macaque', 'tiger', 'crane', 'bear', 'penguin']
base = 'game/assets/sprites/player/paperdoll'
slots = ['chassis', 'head_unit', 'optic_core']

all_valid = True
total_checked = 0

print("=== 1. Chassis & Head_unit 512 Files Verification (Size, Mode, Corner Alphas) ===")
for r in races:
    print(f"\n--- Race: {r} ---")
    for s in ['chassis', 'head_unit']:
        slot_dir = os.path.join(base, r, s)
        files = sorted([f for f in os.listdir(slot_dir) if f.endswith('_512.png')])
        for f in files:
            total_checked += 1
            fp = os.path.join(slot_dir, f)
            with Image.open(fp) as img:
                w, h = img.size
                mode = img.mode
                arr = np.array(img)
                # corners: (0,0), (0, w-1), (h-1, 0), (h-1, w-1)
                tl = arr[0, 0, 3]
                tr = arr[0, w-1, 3]
                bl = arr[h-1, 0, 3]
                br = arr[h-1, w-1, 3]
                corners = (tl, tr, bl, br)
                
                is_ok = (w == 512 and h == 512 and mode == 'RGBA' and all(c == 0 for c in corners))
                if not is_ok:
                    all_valid = False
                status = "PASS" if is_ok else "FAIL"
                print(f"[{status}] {s}/{f}: size=({w},{h}), mode={mode}, corner_alphas={corners}")

print(f"\n=== 2. Optic Core 512 Files Verification ===")
for r in races:
    slot_dir = os.path.join(base, r, 'optic_core')
    files = sorted([f for f in os.listdir(slot_dir) if f.endswith('_512.png')])
    for f in files:
        total_checked += 1
        fp = os.path.join(slot_dir, f)
        with Image.open(fp) as img:
            w, h = img.size
            mode = img.mode
            arr = np.array(img)
            tl = arr[0, 0, 3]
            tr = arr[0, w-1, 3]
            bl = arr[h-1, 0, 3]
            br = arr[h-1, w-1, 3]
            corners = (tl, tr, bl, br)
            is_ok = (w == 512 and h == 512 and mode == 'RGBA' and all(c == 0 for c in corners))
            if not is_ok:
                all_valid = False
            status = "PASS" if is_ok else "FAIL"
            print(f"[{status}] {r}/optic_core/{f}: size=({w},{h}), mode={mode}, corner_alphas={corners}")

print(f"\nTotal files checked: {total_checked}, All valid: {all_valid}")

# 0-QA17 NN 放大否證量測
print("\n=== 3. 0-QA17 NN Upscale Disproof (Repetitive Columns/Rows Analysis) ===")
# 抽取一張代表性圖片：fox chassis paint_fox_orange
src_128_path = os.path.join(base, 'fox', 'chassis', 'paint_fox_orange.png')
lanczos_512_path = os.path.join(base, 'fox', 'chassis', 'paint_fox_orange_512.png')

with Image.open(src_128_path) as s_img:
    s_rgba = s_img.convert('RGBA')
    nn_512 = s_rgba.resize((512, 512), resample=Image.Resampling.NEAREST)

def compute_repeat_rates(img):
    arr = np.array(img) # (512, 512, 4)
    # 針對有內容的非全透明區域，或全圖相鄰比對
    # 重複欄：相鄰兩欄 (arr[:, col] == arr[:, col+1]) 是否整欄完全相同
    col_repeats = 0
    for c in range(511):
        if np.array_equal(arr[:, c], arr[:, c+1]):
            col_repeats += 1
            
    row_repeats = 0
    for r in range(511):
        if np.array_equal(arr[r, :], arr[r+1, :]):
            row_repeats += 1
            
    # 同時針對像素級相鄰像素重複率 (水平方向)
    h_pixel_repeats = np.sum(np.all(arr[:, :-1] == arr[:, 1:], axis=2))
    total_pairs = 512 * 511
    pixel_repeat_rate = h_pixel_repeats / total_pairs
    
    return col_repeats / 511.0, row_repeats / 511.0, pixel_repeat_rate

nn_col, nn_row, nn_pix = compute_repeat_rates(nn_512)
lz_col, lz_row, lz_pix = compute_repeat_rates(Image.open(lanczos_512_path))

print(f"Sample: fox/chassis/paint_fox_orange_512.png")
print(f"  [NEAREST Neighbor baseline (fake upscale)]:")
print(f"    - Identical adjacent full columns rate: {nn_col*100:.2f}% (should be ~75% due to 4x integer replication)")
print(f"    - Identical adjacent full rows rate:    {nn_row*100:.2f}% (should be ~75% due to 4x integer replication)")
print(f"    - Adjacent pixel horizontal repeat:     {nn_pix*100:.2f}% (should be ~75%+)")
print(f"  [LANCZOS Result (our file)]:")
print(f"    - Identical adjacent full columns rate: {lz_col*100:.2f}% (only completely blank edge padding if any)")
print(f"    - Identical adjacent full rows rate:    {lz_row*100:.2f}% (only completely blank edge padding if any)")
print(f"    - Adjacent pixel horizontal repeat:     {lz_pix*100:.2f}% (smooth interpolation, no NN block steps)")
