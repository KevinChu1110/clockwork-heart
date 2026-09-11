from PIL import Image

base = Image.open("/tmp/attack_base.png")
pix = base.load()
for x in [90, 95, 100]:
    for y in [53, 56, 59, 62, 65]:
        p = pix[x, y]
        print(f"x={x}, y={y}: rgba={p}")
