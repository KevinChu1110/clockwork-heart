from PIL import Image

r_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit"
ch_navy = Image.open(f"{r_dir}/chassis/paint_midnight_navy.png").convert("RGBA")

# In midnight navy, let's see where the arm and hand end
w, h = ch_navy.size
data = ch_navy.load()

print("=== Right arm / hand in paint_midnight_navy.png ===")
for y in range(70, 105):
    line = ""
    for x in range(30, 50):
        a = data[x, y][3]
        if a == 0:
            line += " "
        else:
            r, g, b = data[x, y][:3]
            if (r, g, b) == (44, 28, 22) or (r, g, b) == (34, 20, 16):
                line += "#"
            elif (r+g+b)/3 > 150:
                line += "W"
            elif (r+g+b)/3 > 80:
                line += "m"
            else:
                line += "D"
    print(f"y={y:2d}: {line}")
