from PIL import Image

battle_im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/fox_battle.png").convert("RGBA")
bpx = battle_im.load()
assert bpx is not None

# Let's inspect where cyan pixels are:
for y in range(35, 75):
    for x in range(128):
        p = bpx[x, y]
        if p[3] > 80 and p[1] > 140 and p[2] > 140 and p[0] < 140:
            print(f"cyan pixel at ({x}, {y}): {p}")
