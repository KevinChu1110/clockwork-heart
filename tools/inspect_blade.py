import os
from PIL import Image

repo = "/opt/side/bravesoul-game"
r_dir = f"{repo}/game/assets/sprites/player/paperdoll/rabbit"

chassis_ivory = Image.open(f"{r_dir}/chassis/paint_ivory_stock.png")
chassis_navy = Image.open(f"{r_dir}/chassis/paint_midnight_navy.png")
ear = Image.open(f"{r_dir}/head_unit/ear_rabbit_straight.png")
costume = Image.open(f"{r_dir}/costume/costume_nutcracker_guard.png")
blade = Image.open(f"{r_dir}/weapon/wpn_dawn_blade.png")

print("blade bbox:", blade.getbbox())
print("ear bbox:", ear.getbbox())
print("chassis_ivory bbox:", chassis_ivory.getbbox())
print("costume bbox:", costume.getbbox())

# Let's inspect ear edges and white fringe
ear_data = ear.load()
w, h = ear.size
fringes = []
for y in range(h):
    for x in range(w):
        r, g, b, a = ear_data[x, y]
        if 0 < a < 255:
            # Check if it's very bright / white fringe
            if r > 200 and g > 200 and b > 200:
                fringes.append((x, y, r, g, b, a))

print(f"Ear semi-transparent bright pixels (fringe): {len(fringes)}")
if fringes:
    print("Sample fringe pixels:", fringes[:10])

# Check chassis_ivory edges
chassis_data = chassis_ivory.load()
ch_fringes = []
for y in range(h):
    for x in range(w):
        r, g, b, a = chassis_data[x, y]
        if 0 < a < 255:
            if r > 200 and g > 200 and b > 200:
                ch_fringes.append((x, y, r, g, b, a))
print(f"Chassis ivory semi-transparent bright pixels: {len(ch_fringes)}")

# Inspect blade pixels and colors
blade_data = blade.load()
print("\nBlade pixel analysis:")
blade_pixels = []
for y in range(h):
    for x in range(w):
        r, g, b, a = blade_data[x, y]
        if a > 0:
            blade_pixels.append((x, y, r, g, b, a))
print(f"Total non-transparent blade pixels: {len(blade_pixels)}")
# Let's print out what colors exist on the blade
colors = {}
for p in blade_pixels:
    c = (p[2], p[3], p[4])
    colors[c] = colors.get(c, 0) + 1
sorted_colors = sorted(colors.items(), key=lambda x: -x[1])
print("Top blade colors:")
for c, count in sorted_colors[:15]:
    print(f"  RGB{c}: count={count}")
