from PIL import Image

base = Image.open("/tmp/attack_base.png")
pix = base.load()
for x in range(85, 103):
    pts = []
    for y in range(50, 68):
        p = pix[x, y]
        if p[3] > 10:
            pts.append((y, p))
    print(f"x={x}: count={len(pts)}, ys={[y for y, _ in pts]}")
