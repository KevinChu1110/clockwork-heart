from PIL import Image

im = Image.open('game/assets/sprites/player/paperdoll/lion/costume/costume_nutcracker_guard.png').convert('RGBA')
w, h = im.size
pixels = im.load()

# Let's inspect regions where costume has pixels
print("Costume Nutcracker Guard bbox:", im.getbbox())
for y in range(60, 108, 4):
    row_pixels = [pixels[x, y] for x in range(36, 88) if pixels[x, y][3] > 20]
    if row_pixels:
        avg_r = sum(p[0] for p in row_pixels) // len(row_pixels)
        avg_g = sum(p[1] for p in row_pixels) // len(row_pixels)
        avg_b = sum(p[2] for p in row_pixels) // len(row_pixels)
        print(f"Y={y:2d}: count={len(row_pixels):2d}, avg RGB=({avg_r:3d}, {avg_g:3d}, {avg_b:3d})")
