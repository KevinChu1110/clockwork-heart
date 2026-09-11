from PIL import Image

screen = Image.open("/opt/side/bravesoul-game/proofs/combat_feel/rabbit_battle_idle.png").convert("RGB")

for y in range(385, 400):
    for x in range(320, 345, 3):
        r, g, b = screen.getpixel((x, y))
        print(f"({x}, {y}): RGB({r}, {g}, {b}), r-b={r-b}")
