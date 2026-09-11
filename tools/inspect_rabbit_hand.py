from PIL import Image

repo = "/opt/side/bravesoul-game"
r_dir = f"{repo}/game/assets/sprites/player/paperdoll/rabbit"

ch_ivory = Image.open(f"{r_dir}/chassis/paint_ivory_stock.png").convert("RGBA")
ch_navy = Image.open(f"{r_dir}/chassis/paint_midnight_navy.png").convert("RGBA")
blade = Image.open(f"{r_dir}/weapon/wpn_dawn_blade.png").convert("RGBA")

# Let's inspect where the arm and hand are
# Rabbit right arm/hand (character's right, screen's left, x around 35-50, y around 70-95)
# Rabbit left arm/hand (character's left, screen's right, x around 75-90, y around 70-95)

for y in range(70, 95):
    row_ch = ""
    for x in range(32, 52):
        ca = ch_ivory.getpixel((x, y))[3]
        ba = blade.getpixel((x, y))[3]
        if ca > 128 and ba > 128:
            row_ch += "X" # both
        elif ca > 128:
            row_ch += "C" # chassis only
        elif ba > 128:
            row_ch += "B" # blade only
        else:
            row_ch += "."
    print(f"y={y:2d}: {row_ch}")
