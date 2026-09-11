from PIL import Image

l_im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/lion/weapon/wpn_knight_lance.png").convert("RGBA")
w, h = l_im.size
data = l_im.load()

# Let's inspect where pixels exist in wpn_knight_lance.png
print("=== Lion weapon pixels ===")
for y in range(65, 95):
    line = ""
    for x in range(20, 40):
        a = data[x, y][3]
        if a == 0:
            line += " "
        elif a < 128:
            line += "."
        else:
            line += "#"
    if "#" in line:
        print(f"y={y:2d}: {line}")
