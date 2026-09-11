from PIL import Image

idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png").convert("RGBA")
w, h = idle.size

# Let's inspect where the sword is:
# We know from dump_idle_sword_exact.py:
# x from 34 to 92, y from 70 to 125
# Let's see what pixels in that area match r>195, g>195, b>195, abs(r-b)<40
candidates = []
for y in range(h):
    for x in range(w):
        r, g, b, a = idle.getpixel((x, y))
        if a > 128 and r > 195 and g > 195 and b > 195 and abs(r - b) < 40:
            candidates.append((x, y, r, g, b))

# Let's see candidates by region
# Body parts: head is y < 65, ears are y < 50
# Hands/feet/torso
print("Candidates by y:")
for y_band in range(0, 128, 10):
    c_band = [c for c in candidates if y_band <= c[1] < y_band + 10]
    print(f"y in [{y_band}, {y_band+10}): {len(c_band)} pixels")

# Let's inspect y >= 60 pixels
y60_c = [c for c in candidates if c[1] >= 60]
print(f"Candidates with y >= 60: {len(y60_c)}")
# What are their x coords?
for c in y60_c[:10]:
    print(c)
