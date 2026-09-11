from PIL import Image

repo = "/opt/side/bravesoul-game"
r_dir = f"{repo}/game/assets/sprites/player/paperdoll/rabbit"

files = [
    "head_unit/ear_rabbit_straight.png",
    "chassis/paint_ivory_stock.png",
    "chassis/paint_brass_gold.png",
    "chassis/paint_midnight_navy.png",
    "costume/costume_nutcracker_guard.png",
    "costume/costume_royal_parade.png",
    "weapon/wpn_dawn_blade.png",
    "composite_preview_nutcracker.png",
]

for fname in files:
    im = Image.open(f"{r_dir}/{fname}").convert("RGBA")
    w, h = im.size
    data = im.load()
    alpha_0_colors = {}
    border_alpha_0_white = 0
    border_alpha_low_white = 0
    total_a0 = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = data[x, y]
            if a == 0:
                total_a0 += 1
                if r > 150 and g > 150 and b > 150:
                    border_alpha_0_white += 1
            elif a < 64:
                if r > 150 and g > 150 and b > 150:
                    border_alpha_low_white += 1
    print(f"{fname}:")
    print(f"  total a=0: {total_a0}, a=0 with white/bright RGB: {border_alpha_0_white}")
    print(f"  low alpha (1..63) with white/bright RGB: {border_alpha_low_white}")
