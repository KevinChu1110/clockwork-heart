from PIL import Image

r_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit"
ch_ivory = Image.open(f"{r_dir}/chassis/paint_ivory_stock.png").convert("RGBA")
data = ch_ivory.load()

print("=== Right arm / hand in paint_ivory_stock.png ===")
for y in range(70, 96):
    line = ""
    for x in range(32, 48):
        a = data[x, y][3]
        if a == 0:
            line += " "
        else:
            r, g, b = data[x, y][:3]
            lum = (r+g+b)/3
            if lum < 60:
                line += "#"
            elif lum > 180:
                line += "W"
            elif lum > 120:
                line += "m"
            else:
                line += "D"
    print(f"y={y:2d}: {line}")
