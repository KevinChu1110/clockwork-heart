from PIL import Image

core = Image.open("game/assets/sprites/player/paperdoll/macaque/optic_core/core_cyan_emerald.png").convert("RGBA")
print("optic_core size:", core.size, "bbox:", core.getbbox())
# print non-transparent pixels
px = core.load()
for y in range(39, 78):
    for x in range(36, 65):
        if px[x, y][3] > 0:
            print(f"({x},{y}): {px[x, y]}")
