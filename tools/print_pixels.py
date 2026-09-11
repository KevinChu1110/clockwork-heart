from PIL import Image

repo = "/opt/side/bravesoul-game"
r_dir = f"{repo}/game/assets/sprites/player/paperdoll/rabbit"

ch_ivory = Image.open(f"{r_dir}/chassis/paint_ivory_stock.png").convert("RGBA")
blade = Image.open(f"{r_dir}/weapon/wpn_dawn_blade.png").convert("RGBA")

print("--- Blade in region x:32..50, y:70..86 ---")
for y in range(70, 86):
    row = ""
    for x in range(34, 50):
        b = blade.getpixel((x, y))
        if b[3] > 0:
            row += f"[{b[0]:02x}{b[1]:02x}{b[2]:02x}]"
        else:
            row += "........"
    print(f"y={y:2d}: {row}")

print("\n--- Chassis in region x:32..50, y:70..86 ---")
for y in range(70, 86):
    row = ""
    for x in range(34, 50):
        c = ch_ivory.getpixel((x, y))
        if c[3] > 0:
            row += f"[{c[0]:02x}{c[1]:02x}{c[2]:02x}]"
        else:
            row += "........"
    print(f"y={y:2d}: {row}")
