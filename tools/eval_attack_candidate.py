import os
from PIL import Image, ImageChops

POSES_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox"
POSES = ["idle", "telegraph", "attack", "recover", "skill", "hit"]

cand = Image.open("/tmp/test_attack_candidate.png").convert("RGBA")
battle_im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/fox_battle.png").convert("RGBA")

# Measure body bbox excluding y >= 118
px = cand.load()
min_x, min_y, max_x, max_y = 128, 128, -1, -1
for y in range(118):
    for x in range(128):
        if px[x, y][3] > 10:
            if x < min_x: min_x = x
            if x > max_x: max_x = x
            if y < min_y: min_y = y
            if y > max_y: max_y = y
h = max_y - min_y + 1 if max_y >= min_y else 0
print(f"Candidate attack: full_bbox={cand.getbbox()} | body(y<118) bbox=({min_x}, {min_y}, {max_x}, {max_y}) height={h}")

print("\n--- Diff Matrix: candidate attack vs other poses & fox_battle ---")
for name, other_path in [("fox_battle", "/opt/side/bravesoul-game/game/assets/sprites/player/fox_battle.png")] + [(p, os.path.join(POSES_DIR, f"{p}.png")) for p in POSES if p != "attack"]:
    other = Image.open(other_path).convert("RGBA")
    diff = ImageChops.difference(cand, other)
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
    passed_body = "PASS" if body_diff >= 6000 else "FAIL (<6000)"
    passed_leg = "PASS" if leg_diff >= 800 else "FAIL (<800)"
    print(f"candidate vs {name:10s}: body_diff(y<118)={body_diff:5d} px [{passed_body}], leg_diff(92..117)={leg_diff:4d} px [{passed_leg}]")

# Check 8-connected components in pure Python
visited = set()
components = []
for y in range(118):
    for x in range(128):
        if px[x, y][3] > 40 and (x, y) not in visited:
            # BFS 8-connected
            comp = []
            queue = [(x, y)]
            visited.add((x, y))
            while queue:
                cx, cy = queue.pop(0)
                comp.append((cx, cy))
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0: continue
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < 128 and 0 <= ny < 118:
                            if px[nx, ny][3] > 40 and (nx, ny) not in visited:
                                visited.add((nx, ny))
                                queue.append((nx, ny))
            components.append(comp)

print(f"\nConnected components (alpha>40, y<118): {len(components)}")
for i, comp in enumerate(components, 1):
    xs = [x for x, y in comp]
    ys = [y for x, y in comp]
    print(f"  Comp {i}: {len(comp)} px, bbox=({min(xs)}, {min(ys)}, {max(xs)}, {max(ys)})")
