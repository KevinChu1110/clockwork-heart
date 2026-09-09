from PIL import Image

mag = Image.open("game/assets/sprites/player/paperdoll/lion/proof_paperdoll_lion_artisan_navy_magenta.png")
wep = Image.open("game/assets/sprites/player/paperdoll/lion/weapon/wpn_knight_lance.png")
ch = Image.open("game/assets/sprites/player/paperdoll/lion/chassis/paint_midnight_navy.png")

print("Weapon non-zero pixels around bottom left:")
for y in range(115, 128):
    for x in range(20, 36):
        p = wep.getpixel((x, y))
        if p[3] > 0:
            print(f"  Weapon ({x}, {y}): {p}")
