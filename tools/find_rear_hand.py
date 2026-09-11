from PIL import Image

atk = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/attack.png").convert("RGBA")
w, h = atk.size
px = atk.load()

# Left side / hip region: x from 25 to 55, y from 60 to 85
print("Rear hand / hip region (25<=x<=55, 60<=y<=85):")
for y in range(60, 85):
    row = []
    for x in range(25, 55):
        p = px[x, y]
        if p[3] > 30:
            # check skin/metal colors
            row.append(f"{x}:({p[0]},{p[1]},{p[2]})")
    if row:
        print(f"y={y}: min_x={row[0].split(':')[0]}, max_x={row[-1].split(':')[0]}")
