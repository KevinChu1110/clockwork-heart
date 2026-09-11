from PIL import Image

im = Image.open('/tmp/perfect_ivory_clean.png').convert('RGBA')
px = im.load()
w, h = im.size

# Check pixels with a > 0 in the head right area (x > 80, y < 45)
print("Checking pixels in x > 80, y < 45:")
for y in range(45):
    for x in range(80, w):
        r, g, b, a = px[x, y]
        if a > 0:
            # check if isolated (no opaque neighbors in 8 directions)
            nbr_opaque = sum(1 for dx in [-1,0,1] for dy in [-1,0,1] if (dx!=0 or dy!=0) and 0<=x+dx<w and 0<=y+dy<h and px[x+dx, y+dy][3] >= 64)
            if nbr_opaque <= 1:
                print(f"Isolated stray pixel found at ({x}, {y}): color={(r,g,b,a)}")
                im.putpixel((x, y), (0, 0, 0, 0))

im.save('/tmp/perfect_ivory_clean2.png')
