from PIL import Image

screen = Image.open("/opt/side/bravesoul-game/proofs/combat_feel/rabbit_battle_idle.png").convert("RGB")
idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png").convert("RGBA")

scale = 200.0 / 128.0
ox = 224.0
oy = 248.0 # 223 + 25

# Let's test different subsets of blade pixels in idle
# For example, x in [58, 80], y in [75, 96]
blade_pixels = []
for y in range(75, 96):
    for x in range(58, 80):
        r, g, b, a = idle.getpixel((x, y))
        if a > 128 and r > 195 and g > 195 and b > 195 and abs(r - b) < 40:
            blade_pixels.append((x, y, r, g, b))

print(f"Blade pixels in bounding box: {len(blade_pixels)}")

# Map to screen
silvers = 0
browns = 0
rgbs = []
for x, y, _, _, _ in blade_pixels:
    # Screen coord
    # Note: STRETCH_KEEP_ASPECT_CENTERED mapping:
    # A pixel (x, y) covers [x*scale, (x+1)*scale]
    # Center of pixel:
    scx = int(ox + (x + 0.5) * scale)
    scy = int(oy + (y + 0.5) * scale)
    sr, sg, sb = screen.getpixel((scx, scy))
    rgbs.append((sr, sg, sb))
    is_silver = (sr > 185 and sg > 185 and sb > 185 and abs(sr - sb) < 40)
    is_brown = (sr - sb > 50)
    if is_silver:
        silvers += 1
    if is_brown:
        browns += 1

n = len(blade_pixels)
avg_r = sum(c[0] for c in rgbs) / n
avg_g = sum(c[1] for c in rgbs) / n
avg_b = sum(c[2] for c in rgbs) / n
print(f"Sampled {n} pixels:")
print(f"Silver: {silvers} ({silvers/n*100:.1f}%), Brown: {browns} ({browns/n*100:.1f}%)")
print(f"Average RGB: ({avg_r:.1f}, {avg_g:.1f}, {avg_b:.1f})")
