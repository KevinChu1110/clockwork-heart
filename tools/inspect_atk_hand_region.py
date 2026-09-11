from PIL import Image

atk = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/attack.png").convert("RGBA")
w, h = atk.size
px = atk.load()

# Let's inspect x >= 70, y from 40 to 80
print("Attack sprite forward arm/hand region (x>=75, 45<=y<=75):")
for y in range(45, 75):
    row = []
    for x in range(75, 105):
        if x < w and y < h:
            p = px[x, y]
            if p[3] > 20:
                row.append(f"{x}:({p[0]},{p[1]},{p[2]},{p[3]})")
    if row:
        print(f"y={y}: " + " ".join(row[:4]) + (" ... " + row[-1] if len(row) > 4 else ""))
