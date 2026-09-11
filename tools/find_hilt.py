from PIL import Image

idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png").convert("RGBA")
# Let's inspect all non-white/non-cream pixels around the waist/hips
for y in range(65, 105):
    for x in range(25, 55):
        r, g, b, a = idle.getpixel((x, y))
        if a > 128:
            # check if brown/gold
            if r > 100 and g < 160 and b < 100:
                print(f"idle({x}, {y}) = ({r}, {g}, {b}) [brown/gold hilt]")
