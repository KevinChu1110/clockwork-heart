from PIL import Image
ivory = Image.open('game/assets/sprites/player/paperdoll/lion/chassis/paint_ivory_stock.png').convert('RGBA')
for x in range(45, 60, 3):
    print(f"  X={x}: {ivory.getpixel((x, 120))}")
