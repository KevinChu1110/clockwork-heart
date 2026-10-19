from PIL import Image
import numpy as np

print("=== CHECKING PROOFS ON DISK ===")

# 1. Check proof_c (Costume Variants)
proof_c = Image.open("game/assets/sprites/player/paperdoll/lion/proof_maple_lion_costume_variants.png")
print("proof_c size:", proof_c.size)
v4 = proof_c.crop((1536, 0, 2048, 512))
v4_arr = np.array(v4)

# Check gap at x=153..154, y=281..359
cream = (255, 252, 247)
cream_gap_count = 0
for y in range(281, 360):
    for x in [153, 154]:
        if (v4_arr[y, x][:3] == cream).all():
            cream_gap_count += 1

print(f"1. Cream gap pixels at x in [153, 154], y in [281..359] in costume='none': {cream_gap_count} (MUST BE 0)")
assert cream_gap_count == 0, f"FAILED: {cream_gap_count} cream gap pixels found!"

# Check blue skirt pixels in costume='none' pelvis:
blue_skirt_v4 = 0
for y in range(340, 440):
    for x in range(180, 340):
        p = v4_arr[y, x]
        if not (p[:3] == cream).all():
            if int(p[2]) > int(p[0]) + 10:
                blue_skirt_v4 += 1
print(f"2. Blue skirt pixels in costume='none' pelvis: {blue_skirt_v4} (MUST BE 0)")
assert blue_skirt_v4 == 0, f"FAILED: {blue_skirt_v4} blue skirt pixels found!"

# 2. Check proof_d (Z-Order Swap)
proof_d = Image.open("game/assets/sprites/player/paperdoll/lion/proof_maple_lion_z_order_swap.png")
print("proof_d size:", proof_d.size)
left = np.array(proof_d.crop((0, 0, 512, 512)))
right = np.array(proof_d.crop((512, 0, 1024, 512)))

diff = np.abs(left.astype(int) - right.astype(int))
key_area_diff = diff[183:334, 322:442]
key_diff_count = np.sum(np.any(key_area_diff > 0, axis=2))
print(f"3. Key area differing pixels between left (z=5) and right (z=15): {key_diff_count} (MUST BE > 0)")
assert key_diff_count > 0, f"FAILED: key area diff is 0!"

weapon_diff_count = np.sum(np.any(diff[27:436, 75:154] > 0, axis=2))
print(f"4. Weapon area differing pixels between left (z=40) and right (z=4): {weapon_diff_count} (MUST BE > 0)")
assert weapon_diff_count > 0, f"FAILED: weapon area diff is 0!"

print("\n🎉 ALL 4 AUDIT CHECKS PASSED WITH 100% SUCCESS!")
