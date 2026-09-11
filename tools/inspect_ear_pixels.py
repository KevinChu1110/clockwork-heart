from PIL import Image

r_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit"
ear = Image.open(f"{r_dir}/head_unit/ear_rabbit_straight.png").convert("RGBA")
ch_navy = Image.open(f"{r_dir}/chassis/paint_midnight_navy.png").convert("RGBA")

ear.save("/tmp/ear_alone.png")
ch_navy.save("/tmp/ch_navy_alone.png")

# Let's inspect the pixels of ear at the top edge (y=7..20) and outer edge (x=41..83)
# Are there any alpha edges that look white when blended?
ear_data = ear.load()
for y in range(7, 25):
    line = ""
    for x in range(41, 84):
        a = ear_data[x, y][3]
        if a == 0:
            line += " "
        elif a < 255:
            r, g, b = ear_data[x, y][:3]
            line += "o" if (r+g+b)/3 > 180 else "x"
        else:
            line += "#"
    print(f"y={y:2d}: {line}")
