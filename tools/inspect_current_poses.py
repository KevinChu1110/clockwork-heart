import os
from PIL import Image, ImageChops

POSES_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox"
POSES = ["idle", "telegraph", "attack", "recover", "skill", "hit"]

print("--- Current Poses on Disk ---")
imgs = {}
for p in POSES:
    path = os.path.join(POSES_DIR, f"{p}.png")
    im = Image.open(path).convert("RGBA")
    imgs[p] = im
    px = im.load()
    min_x, min_y, max_x, max_y = 128, 128, -1, -1
    for y in range(118):
        for x in range(128):
            if px[x, y][3] > 10:
                if x < min_x: min_x = x
                if x > max_x: max_x = x
                if y < min_y: min_y = y
                if y > max_y: max_y = y
    h = max_y - min_y + 1 if max_y >= min_y else 0
    print(f"{p:10s}: full_bbox={im.getbbox()} | body(y<118) bbox=({min_x}, {min_y}, {max_x}, {max_y}) height={h}")

battle_im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/fox_battle.png").convert("RGBA")
print("\n--- attack.png vs fox_battle and other poses (body y<118 diff) ---")
atk_im = imgs["attack"]
for name, other in [("fox_battle", battle_im)] + [(p, imgs[p]) for p in POSES if p != "attack"]:
    diff = ImageChops.difference(atk_im, other)
    dpx = diff.load()
    body_diff = 0
    leg_diff = 0
    for y in range(128):
        for x in range(128):
            if max(dpx[x, y]) > 10:
                if y < 118:
                    body_diff += 1
                if 92 <= y < 118:
                    leg_diff += 1
    print(f"attack vs {name:10s}: body_diff(y<118)={body_diff} px, leg_diff(92<=y<118)={leg_diff} px")
