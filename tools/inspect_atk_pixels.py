from PIL import Image

atk = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/attack.png").convert("RGBA")
w, h = atk.size

# Let's inspect non-transparent pixels
print("atk size:", w, h)
print("bbox:", atk.getbbox())

# Let's check where the fist / arm extends:
# in attack pose, the arm extends forward. Let's find rows and columns of the front hand.
# Let's list pixels on the right side or left side:
px = atk.load()
for y in range(h):
    row_pixels = [(x, px[x, y]) for x in range(w) if px[x, y][3] > 30]
    if row_pixels:
        min_x = min(p[0] for p in row_pixels)
        max_x = max(p[0] for p in row_pixels)
        if max_x > 80: # right side extension
            # print sample
            print(f"y={y}: x from {min_x} to {max_x}, rightmost px={px[max_x, y]}")
