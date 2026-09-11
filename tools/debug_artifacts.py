from PIL import Image
from typing import cast

atk = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/attack.png")
tele = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/telegraph.png")

px = tele.load()
assert px is not None
white_pts = []
for y in range(110, 128):
    for x in range(128):
        p = cast(tuple[int, int, int, int], px[x, y])
        if p[3] > 100 and p[0] > 200 and p[1] > 200 and p[2] > 200:
            white_pts.append((x, y))

print("White points in telegraph ground:", len(white_pts))
if white_pts:
    print("Sample:", white_pts[:5])

# In attack, what rectangular block artifact is overlapping the hem?
a_px = atk.load()
assert a_px is not None
print("Check attack y=100..128:")
for y in range(100, 125, 4):
    non_zero = sum(1 for x in range(128) if cast(tuple[int, int, int, int], a_px[x, y])[3] > 0)
    print(f"  y={y}: non_zero={non_zero}")
