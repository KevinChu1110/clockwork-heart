from PIL import Image

im = Image.open('game/assets/sprites/player/poses/macaque/attack.png').convert('RGBA')
print("Macaque attack.png size:", im.size, "bbox:", im.getbbox())

# Let's check colors in hands/torso
arr = im.load()
for y in range(im.size[1]):
    row = ""
    has_px = False
    for x in range(im.size[0]):
        if arr[x, y][3] > 50:
            has_px = True
    # just checking bounds
