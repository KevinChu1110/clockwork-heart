# Let's search what input (r, g, b) produces output (240, 220, 172)
from test_exact_math import test_shader

target = (240, 220, 172)
best_diff = 999
best_in = None
for r in range(150, 256):
    for g in range(150, 256):
        for b in range(100, 256):
            out = test_shader(r, g, b, sat=1.22, con=1.12, bri=1.05)
            diff = abs(out[0] - target[0]) + abs(out[1] - target[1]) + abs(out[2] - target[2])
            if diff < best_diff:
                best_diff = diff
                best_in = (r, g, b)
                if diff < 1:
                    break
        if best_diff < 1:
            break
    if best_diff < 1:
        break

print(f"To get output {target}, input must be: {best_in} (diff={best_diff:.1f})")
if best_in:
    print(f"Input r-b was: {best_in[0] - best_in[2]}")
