from PIL import Image

screen = Image.open("/opt/side/bravesoul-game/proofs/combat_feel/rabbit_battle_idle.png").convert("RGB")
idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png").convert("RGBA")

scale = 200.0 / 128.0
ox = 224.0
oy = 248.0

# What if 276 is the number of pixels on the SCREEN that correspond to the blade?
# Let's check:
# In idle, if blade has ~110-120 pixels, on screen it's ~270 pixels!
# Or in idle, what if blade + hilt or blade has a region?
# Let's test checking every pixel on the screen within the player rect:
# For every screen pixel (sx, sy), find its source texture pixel (tx, ty) = ((sx - ox)/scale, (sy - oy)/scale)
# If idle[tx, ty] is silver in the blade region:
blade_idle_pixels = set()
for y in range(70, 98):
    for x in range(58, 83):
        r, g, b, a = idle.getpixel((x, y))
        if a > 128 and r > 195 and g > 195 and b > 195 and abs(r - b) < 40:
            blade_idle_pixels.add((x, y))

print(f"Blade idle pixels: {len(blade_idle_pixels)}")

# Now find all screen pixels whose nearest source pixel is in blade_idle_pixels:
# Or screen pixels where (int((sx-ox)/scale), int((sy-oy)/scale)) in blade_idle_pixels:
for y_min, y_max, x_min, x_max in [
    (75, 95, 60, 80),
    (75, 96, 58, 80),
    (74, 95, 59, 81),
    (76, 94, 61, 78)
]:
    b_idle = set()
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            r, g, b, a = idle.getpixel((x, y))
            if a > 128 and r > 195 and g > 195 and b > 195 and abs(r - b) < 40:
                b_idle.add((x, y))
    
    screen_pts = []
    silvers = 0
    browns = 0
    rgbs = []
    # Screen bounding box:
    sx0 = int(ox + x_min * scale)
    sx1 = int(ox + (x_max + 1) * scale)
    sy0 = int(oy + y_min * scale)
    sy1 = int(oy + (y_max + 1) * scale)
    for sy in range(sy0, sy1 + 1):
        for sx in range(sx0, sx1 + 1):
            tx = int((sx - ox) / scale)
            ty = int((sy - oy) / scale)
            if (tx, ty) in b_idle:
                sr, sg, sb = screen.getpixel((sx, sy))
                screen_pts.append((sx, sy))
                rgbs.append((sr, sg, sb))
                if sr > 185 and sg > 185 and sb > 185 and abs(sr - sb) < 40:
                    silvers += 1
                if sr - sb > 50:
                    browns += 1
    if screen_pts:
        ar = sum(c[0] for c in rgbs) / len(screen_pts)
        ag = sum(c[1] for c in rgbs) / len(screen_pts)
        ab = sum(c[2] for c in rgbs) / len(screen_pts)
        print(f"y: {y_min}-{y_max}, x: {x_min}-{x_max} -> screen count: {len(screen_pts)}, silver: {silvers}, brown: {browns}, avg: ({ar:.1f}, {ag:.1f}, {ab:.1f})")
