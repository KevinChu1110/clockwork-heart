from PIL import Image

im_orig = Image.open("/tmp/attack_orig.png")
pix = im_orig.load()
for y in range(48, 72):
    xs = [x for x in range(70, 105) if pix[x, y][3] > 10]
    if xs:
        print(f"y={y}: xs min={min(xs)}, max={max(xs)}, count={len(xs)}")
