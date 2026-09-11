from PIL import Image
import numpy as np

# Load rabbit idle
idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png").convert("RGBA")
w, h = idle.size

# Load rabbit_battle_idle screenshot
screen = Image.open("/opt/side/bravesoul-game/proofs/combat_feel/rabbit_battle_idle.png").convert("RGB")

print("Idle size:", idle.size)
print("Screen size:", screen.size)

# Mapping parameters
scale = 200.0 / 128.0
origin_x = 224.0
origin_y = 223.0 + 25.0 # (250 - 200) / 2

# Let's inspect candidate silver pixels in the sword area
# Where is the dawn sword blade in idle.png?
# Let's find all pixels in idle where r>195, g>195, b>195, abs(r-b)<40, a>128
# And see which region corresponds to the 276 pixels!
all_silver = []
for y in range(h):
    for x in range(w):
        r, g, b, a = idle.getpixel((x, y))
        if a > 128 and r > 195 and g > 195 and b > 195 and abs(r - b) < 40:
            all_silver.append((x, y, r, g, b))

print(f"Total silver in whole idle.png: {len(all_silver)}")

# Let's see if we isolate the sword region
# The sword is in the lower right or right side. Let's inspect x and y ranges.
for y_min in [60, 65, 70, 72, 75]:
    for x_min in [30, 35, 40, 45, 50, 55, 60, 65]:
        subset = [p for p in all_silver if p[0] >= x_min and p[1] >= y_min]
        if abs(len(subset) - 276) < 20:
            print(f"y_min={y_min}, x_min={x_min} -> count={len(subset)}")

# Let's also check if the 276 pixels come from mapped screen pixels!
# Notice: in 128x128, a region scaled by 200/128 will cover more screen pixels!
# Wait! 276 pixels: is 276 the number of source pixels in 128x128, or the number of mapped screen pixels?
# Let's check:
# "實測兔子晨曦長劍刃身 276 個像素："
# "依 player_body 的 STRETCH_KEEP_ASPECT_CENTERED 映射（scale=200/128、origin 由 get_global_rect 算）到成品座標取值。"
