from PIL import Image

idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png").convert("RGBA")
print("idle.png at (69, 90):", idle.getpixel((69, 90)))
print("idle.png at (68, 90):", idle.getpixel((68, 90)))
print("idle.png at (67, 90):", idle.getpixel((67, 90)))
