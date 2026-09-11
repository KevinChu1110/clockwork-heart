import os
import sys
from PIL import Image, ImageChops

POSES_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox"
POSES = ["idle", "telegraph", "attack", "recover", "skill", "hit"]

sys.path.insert(0, "/opt/side/bravesoul-game")
from tools.generate_fox_combat_poses import measure_staff_linearity, measure_shadow_rows

idle_img = Image.open(os.path.join(POSES_DIR, "idle.png")).convert("RGBA")
idle_staff_resid = measure_staff_linearity(idle_img)
print(f"Idle staff linearity resid: {idle_staff_resid:.4f} (2x threshold: {idle_staff_resid*2:.4f})")

for p in POSES:
    img = Image.open(os.path.join(POSES_DIR, f"{p}.png")).convert("RGBA")
    diff = ImageChops.difference(idle_img, img)
    diff_data = list(diff.convert("L").getdata())
    diff_px = sum(1 for x in diff_data if x > 10)
    
    resid = measure_staff_linearity(img)
    shadow = measure_shadow_rows(img)
    
    px = img.load()
    min_x, min_y, max_x, max_y = 128, 128, -1, -1
    for y in range(118):
        for x in range(128):
            if px[x, y][3] > 10:
                if x < min_x: min_x = x
                if x > max_x: max_x = x
                if y < min_y: min_y = y
                if y > max_y: max_y = y
    h = max_y - min_y + 1
    print(f"[{p:10s}] top_y={min_y:2d}, bot_y={max_y:2d}, h={h:3d} | diff_vs_idle={diff_px:5d} | staff_resid={resid:.2f} | shadow={shadow}")
