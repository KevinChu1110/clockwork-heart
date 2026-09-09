from PIL import Image

im = Image.open('game/assets/sprites/player/paperdoll/lion/costume/costume_nutcracker_guard.png')
print("Lion costume size:", im.size, "bbox:", im.getbbox())
# Let's inspect where it sits relative to lion chassis
ch = Image.open('game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold.png')
print("Lion chassis bbox:", ch.getbbox())

# Let's see pixels where costume has opacity
w, h = im.size
cost_pts = []
for y in range(h):
    for x in range(w):
        if im.getpixel((x, y))[3] > 20:
            cost_pts.append((x, y))

print("Total costume points:", len(cost_pts))
min_x = min(p[0] for p in cost_pts)
max_x = max(p[0] for p in cost_pts)
min_y = min(p[1] for p in cost_pts)
max_y = max(p[1] for p in cost_pts)
print(f"X range: {min_x}..{max_x}, Y range: {min_y}..{max_y}")
