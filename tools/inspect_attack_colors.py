from PIL import Image

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/attack.png")
pix = im.load()
for x in range(106, 122):
    row_info = []
    for y in range(50, 72):
        p = pix[x, y]
        if p[3] > 10:
            row_info.append(f"y={y}:({p[0]},{p[1]},{p[2]},{p[3]})")
    print(f"x={x}: {' | '.join(row_info)}")
