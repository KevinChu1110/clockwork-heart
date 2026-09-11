from PIL import Image

ear = Image.open("game/assets/sprites/player/paperdoll/macaque/head_unit/ear_macaque_coaxial.png").convert("RGBA")
print("Ear bbox:", ear.getbbox())
px = ear.load()
w, h = ear.size

# Check what pixels exist in ear slice
for y in range(h):
    for x in range(w):
        if px[x, y][3] > 0:
            # check if it is outside ears (ears are x < 35 or x > 75, or helmet crown)
            if 38 <= x <= 72 and 25 <= y <= 55:
                print(f"Suspicious interior pixel in ear slice at ({x}, {y}): {px[x, y]}")
