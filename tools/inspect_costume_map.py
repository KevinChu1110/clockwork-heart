from PIL import Image

nut = Image.open('game/assets/sprites/player/paperdoll/lion/costume/costume_nutcracker_guard.png').convert('RGBA')
ch = Image.open('game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold.png').convert('RGBA')

w, h = nut.size
print("Nutcracker costume alpha map:")
for y in range(60, 109, 2):
    line = ""
    for x in range(36, 89):
        p = nut.getpixel((x, y))
        line += "#" if p[3] > 100 else ("." if p[3] > 20 else " ")
    print(f"Y={y:3d}: {line}")
