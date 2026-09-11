from PIL import Image

r_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit"
ch_ivory = Image.open(f"{r_dir}/chassis/paint_ivory_stock.png").convert("RGBA")

print("=== Screen right hand in paint_ivory_stock.png ===")
for y in range(75, 90):
    row = ""
    for x in range(78, 90):
        c = ch_ivory.getpixel((x, y))
        if c[3] > 0:
            row += f"[{c[0]:02x}{c[1]:02x}{c[2]:02x}]"
        else:
            row += "........"
    print(f"y={y:2d}: {row}")
