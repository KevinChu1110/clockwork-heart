from PIL import Image
import numpy as np

print("=== VERIFYING FIX 1: PURE MECHANICAL CHASSIS (NO BLUE SKIRT) ===")
for p_name in ["paint_brass_gold", "paint_ivory_stock", "paint_midnight_navy"]:
    b_path = f"game/assets/sprites/player/paperdoll/lion/maple_parts/body/{p_name}.png"
    b_img = Image.open(b_path).convert("RGBA")
    b_arr = np.array(b_img)

    # Pelvis blue count: y: 340..440, x: 180..340, where B > R + 10 and alpha > 100
    pelvis = b_arr[340:440, 180:340]
    blue_count = 0
    for y in range(340, 440):
        for x in range(180, 340):
            p = b_arr[y, x]
            if p[3] > 100 and int(p[2]) > int(p[0]) + 10:
                blue_count += 1
    print(f"  [{p_name}] Pelvis blue pixels (B > R + 10): {blue_count} (Must be 0)")
    assert blue_count == 0, f"FAILED: {p_name} has {blue_count} blue pixels in pelvis!"

    # Core pixel check: (236, 300) must be glowing cyan
    core_p = b_arr[300, 236]
    print(f"  [{p_name}] Chest core at (236, 300): RGBA={core_p.tolist()}")
    assert core_p[1] > 200 and core_p[2] > 180, "FAILED: Core is not glowing cyan!"

print("\n=== VERIFYING FIX 2: BARE BODY LANCE/HAND SEAM (NO GAP AT x=153..154) ===")
b_img = Image.open("game/assets/sprites/player/paperdoll/lion/maple_parts/body/paint_brass_gold.png").convert("RGBA")
b_arr = np.array(b_img)
gap_pixels = 0
for y in range(281, 360):
    for x in [153, 154]:
        if b_arr[y, x, 3] < 100:
            gap_pixels += 1
print(f"  Body transparent pixels at x in [153, 154], y in [281..359]: {gap_pixels} (Must be 0)")
assert gap_pixels == 0, f"FAILED: Body has {gap_pixels} gap pixels!"

print("\n=== VERIFYING FIX 3: DYNAMIC Z-ORDER KEY OVERLAP & SEPARATION ===")
head = Image.open("game/assets/sprites/player/paperdoll/lion/maple_parts/head_unit/ear_lion_gilded_mane_brass.png").convert("RGBA")
key = Image.open("game/assets/sprites/player/paperdoll/lion/maple_parts/winding_key/key_classic_brass.png").convert("RGBA")
# key at (322, 183), head at (131, 51)
h_canvas = np.zeros((512, 512), dtype=bool)
h_canvas[51:51+head.height, 131:131+head.width] = (np.array(head)[:, :, 3] > 100)
k_canvas = np.zeros((512, 512), dtype=bool)
k_canvas[183:183+key.height, 322:322+key.width] = (np.array(key)[:, :, 3] > 100)
overlap_h_k = h_canvas & k_canvas
print(f"  Mane and Key overlap pixels: {np.sum(overlap_h_k)} (Mane does NOT bake in key)")

# Check body and key overlap at socket (342, 296):
b_canvas = (b_arr[:, :, 3] > 100)
overlap_b_k = b_canvas & k_canvas
print(f"  Body and Key overlap pixels at back socket: {np.sum(overlap_b_k)} (Provides depth for Z-Order swap)")
assert np.sum(overlap_b_k) > 10, "FAILED: Body and key must overlap at socket for Z-Order depth!"

print("\n🎉 ALL UNIT ASSERTIONS PASSED PERFECTLY!")
