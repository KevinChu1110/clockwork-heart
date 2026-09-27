from PIL import Image

img = Image.open('/opt/side/bravesoul-game/proofs/creation-tabs-i18n/proof_creation_launch_zh_TW.png')

found_pixels = []
for y in range(500, 715):
    for x in range(640, 1240):
        px = img.getpixel((x, y))
        r, g, b = px[0], px[1], px[2]
        if (r, g, b) != (255, 255, 255) and (r, g, b) != (255, 253, 248):
            found_pixels.append((x, y, (r, g, b)))

print("Total non-white pixels found in 640..1240, 500..715:", len(found_pixels))
if found_pixels:
    min_x = min(p[0] for p in found_pixels)
    max_x = max(p[0] for p in found_pixels)
    min_y = min(p[1] for p in found_pixels)
    max_y = max(p[1] for p in found_pixels)
    print(f"Bounding box: x=({min_x}..{max_x}), y=({min_y}..{max_y})")
