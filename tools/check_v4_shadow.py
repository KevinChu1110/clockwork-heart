from PIL import Image

v4 = Image.open("/tmp/v4_dawn_blade.png")
w, h = v4.size
data = v4.load()

semi_pixels = []
for y in range(h):
    for x in range(w):
        a = data[x, y][3]
        if 0 < a < 255:
            semi_pixels.append((x, y, data[x, y]))

print(f"Total semi-transparent shadow pixels in final_v4: {len(semi_pixels)}")
if semi_pixels:
    print("Sample semi pixels:", semi_pixels[:10])
