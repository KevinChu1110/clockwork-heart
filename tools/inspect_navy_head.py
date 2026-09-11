from PIL import Image

r_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit"
ch_navy = Image.open(f"{r_dir}/chassis/paint_midnight_navy.png").convert("RGBA")

# Let's inspect the head pixels in paint_midnight_navy
# In midnight navy, the body is deep navy, but what color is the head?
ch_data = ch_navy.load()
for y in range(42, 65):
    line = ""
    for x in range(34, 94):
        a = ch_data[x, y][3]
        if a == 0:
            line += " "
        else:
            r, g, b = ch_data[x, y][:3]
            # check brightness
            lum = (r + g + b) / 3
            if lum > 180:
                line += "W" # White/Ivory
            elif lum > 100:
                line += "m" # medium
            else:
                line += "D" # Dark/Navy
    print(f"y={y:2d}: {line}")
