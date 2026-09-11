from PIL import Image

atk = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/attack.png")
px = atk.load()
assert px is not None

print("Attack bbox:", atk.getbbox())
for x in range(100, 128):
    alphas = []
    for y in range(128):
        p = px[x, y]
        if p[3] > 0:
            alphas.append(p[3])
    if alphas:
        print(f"x={x}: count={len(alphas)}, max_a={max(alphas)}, min_a={min(alphas)}")
