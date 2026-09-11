from PIL import Image

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/weapon/wpn_spring_claws.png")
pix = im.load()
for y in [82, 85, 88, 91, 94]:
    print(f"--- y={y} ---")
    for x in range(20, 42):
        p = pix[x, y]
        if p[3] > 0:
            print(f"  x={x}: rgba=({p[0]},{p[1]},{p[2]},{p[3]})")
