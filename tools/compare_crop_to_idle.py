from PIL import Image, ImageChops
import numpy as np

screen_crop = Image.open("/tmp/player_drawn_crop_grade_off.png").convert("RGB")
idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png").convert("RGBA")

# Resize idle to 200x200 with bilinear (LINEAR in Godot)
idle_linear = idle.resize((200, 200), Image.BILINEAR)

# Compare RGB where idle alpha > 200
diffs = []
for y in range(200):
    for x in range(200):
        ia = idle_linear.getpixel((x, y))[3]
        if ia > 240:
            sp = screen_crop.getpixel((x, y))
            ip = idle_linear.getpixel((x, y))[:3]
            diff = max(abs(sp[i] - ip[i]) for i in range(3))
            diffs.append((diff, sp, ip, (x, y)))

max_diff = max(d[0] for d in diffs)
print(f"Max diff between screen crop and idle_linear where opaque: {max_diff}")
# Find top diffs
diffs.sort(key=lambda x: -x[0])
for d in diffs[:10]:
    print(f"diff={d[0]} at {d[3]}: screen={d[1]}, idle_linear={d[2]}")
