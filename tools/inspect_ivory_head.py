from PIL import Image

r_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit"
ch_ivory = Image.open(f"{r_dir}/chassis/paint_ivory_stock.png").convert("RGBA")

ch_data = ch_ivory.load()
for y in range(42, 65):
    line = ""
    for x in range(34, 94):
        a = ch_data[x, y][3]
        if a == 0:
            line += " "
        else:
            r, g, b = ch_data[x, y][:3]
            lum = (r + g + b) / 3
            if lum > 200:
                line += "W" # White/Ivory
            elif lum > 120:
                line += "m" # medium
            else:
                line += "D" # Dark
    print(f"y={y:2d}: {line}")
