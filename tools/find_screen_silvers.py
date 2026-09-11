from PIL import Image

screen = Image.open("/opt/side/bravesoul-game/proofs/combat_feel/rabbit_battle_idle.png").convert("RGB")
w, h = screen.size

# Let's find all pixels in the entire screen that are silver:
# r > 185, g > 185, b > 185, abs(r-b) < 40
silver_pixels = []
for y in range(h):
    for x in range(w):
        r, g, b = screen.getpixel((x, y))
        if r > 185 and g > 185 and b > 185 and abs(r - b) < 40:
            silver_pixels.append((x, y, r, g, b))

print(f"Total silver pixels on screen (grade OFF): {len(silver_pixels)}")

# Look at x in [200, 500], y in [200, 600]
player_silvers = [p for p in silver_pixels if 200 <= p[0] <= 500 and 200 <= p[1] <= 600]
print(f"Player area silver pixels: {len(player_silvers)}")

# Let's inspect clusters of player silvers
# Where are the blade pixels?
# In idle.png, the blade has r-b ~ 28.
# Let's check clusters by y
by_y = {}
for x, y, r, g, b in player_silvers:
    by_y.setdefault(y, []).append((x, r, g, b))

for y in sorted(by_y.keys()):
    xs = [item[0] for item in by_y[y]]
    if len(xs) > 3:
        avg_r = sum(item[1] for item in by_y[y]) / len(xs)
        avg_g = sum(item[2] for item in by_y[y]) / len(xs)
        avg_b = sum(item[3] for item in by_y[y]) / len(xs)
        print(f"y={y:3d}: count={len(xs):2d}, x in [{min(xs):3d}, {max(xs):3d}], avg=({avg_r:.1f}, {avg_g:.1f}, {avg_b:.1f})")
