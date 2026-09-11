from PIL import Image

cand = Image.open("/tmp/test_attack_candidate_v2.png").convert("RGBA")
px = cand.load()
assert px is not None

print("Checking edge alphas (Rule 12a):")
for name, col_idx in [("x=0", 0), ("x=1", 1), ("x=126", 126), ("x=127", 127)]:
    vals = [px[col_idx, y][3] for y in range(128)]
    print(f"{name}: max alpha={max(vals)}, count>10={sum(1 for v in vals if v > 10)}")

vals_y0 = [px[x, 0][3] for x in range(128)]
print(f"y=0: max alpha={max(vals_y0)}, count>10={sum(1 for v in vals_y0 if v > 10)}")
