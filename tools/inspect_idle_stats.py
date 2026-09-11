from PIL import Image

idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png").convert("RGBA")

# Let's inspect source_pts for rabbit in box (60, 70, 80, 96)
box = (60, 70, 80, 96)
source_pts = []
for y in range(box[1], box[3] + 1):
    for x in range(box[0], box[2] + 1):
        r, g, b, a = idle.getpixel((x, y))
        if a > 128 and r > 195 and g > 195 and b > 195 and abs(r - b) < 40:
            source_pts.append((x, y, r, g, b))

print(f"Total source_pts: {len(source_pts)}")
silvers = 0
browns = 0
for x, y, r, g, b in source_pts:
    if r > 185 and g > 185 and b > 185 and abs(r - b) < 40:
        silvers += 1
    if r - b > 50:
        browns += 1

print(f"In idle.png itself:")
print(f"Silver (>185, |r-b|<40): {silvers}/{len(source_pts)} ({silvers/len(source_pts)*100:.1f}%)")
print(f"Warm (r-b>50): {browns}/{len(source_pts)} ({browns/len(source_pts)*100:.1f}%)")
avg_r = sum(p[2] for p in source_pts) / len(source_pts)
avg_g = sum(p[3] for p in source_pts) / len(source_pts)
avg_b = sum(p[4] for p in source_pts) / len(source_pts)
print(f"Average RGB: ({avg_r:.1f}, {avg_g:.1f}, {avg_b:.1f}), r-b={avg_r-avg_b:.1f}")
