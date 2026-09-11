import sys
sys.path.insert(0, '/opt/side/bravesoul-game')
from PIL import Image
from tools.measure_speckle import interior_speckle

im = Image.open('/tmp/perfect_ivory.png').convert('RGBA')
w, h = im.size
px = im.load()

# Remove isolated stray dark points on arms (x < 42 or x > 75, y: 70..105)
isolated_arms = [
    (35, 77), (34, 79), (76, 83), (28, 88), (30, 91), (34, 92),
    (41, 93), (87, 93), (76, 94), (86, 98), (38, 99), (79, 99),
    (80, 99), (39, 100), (31, 101), (38, 102), (85, 102), (84, 103)
]

for x, y in isolated_arms:
    # check if surrounded mostly by opaque light pixels
    nbrs = []
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h and px[nx, ny][3] >= 128:
            if max(px[nx, ny][:3]) >= 150:
                nbrs.append(px[nx, ny][:3])
    if nbrs:
        avg_c = tuple(int(sum(c[i] for c in nbrs)/len(nbrs)) for i in range(3))
        im.putpixel((x, y), (*avg_c, 255))

out_p = '/tmp/perfect_ivory_clean.png'
im.save(out_p)
print(f"Cleaned stray arm pixels, saved to {out_p}")
interior_speckle(out_p)
