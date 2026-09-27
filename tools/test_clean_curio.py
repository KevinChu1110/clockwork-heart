from PIL import Image, ImageFilter
import numpy as np

# Recreate curio without in-place flood fill bug
W, H = 128, 128
ocx, ocy = 104.0, 60.0

curio_raw = Image.new("RGBA", (W, H), (0, 0, 0, 0))

# 1. Outer Brass Orbital Ring (ellipse tilted at -20 deg)
for y in range(int(ocy - 16), int(ocy + 17)):
    for x in range(int(ocx - 18), int(ocx + 19)):
        dx = x - ocx
        dy = y - ocy
        rad = np.radians(-20)
        rx = dx * np.cos(rad) - dy * np.sin(rad)
        ry = dx * np.sin(rad) + dy * np.cos(rad)
        d_ring = (rx / 14.0)**2 + (ry / 7.0)**2
        if abs(d_ring - 1.0) <= 0.22:
            spec = max(0.0, 1.0 - abs(rx) / 14.0)
            curio_raw.putpixel((x, y), (int(212 + 35 * spec), int(160 + 30 * spec), int(23 + 45 * spec), 255))

# Inner Orbital Ring (tilted at 45 deg)
for y in range(int(ocy - 12), int(ocy + 13)):
    for x in range(int(ocx - 14), int(ocx + 15)):
        dx = x - ocx
        dy = y - ocy
        rad = np.radians(45)
        rx = dx * np.cos(rad) - dy * np.sin(rad)
        ry = dx * np.sin(rad) + dy * np.cos(rad)
        d_ring = (rx / 9.5)**2 + (ry / 4.8)**2
        if abs(d_ring - 1.0) <= 0.25:
            spec = max(0.0, 1.0 - abs(rx) / 9.5)
            curio_raw.putpixel((x, y), (int(180 + 30 * spec), int(140 + 25 * spec), int(30 + 40 * spec), 255))

# Central Sun Sphere (radius 4.5)
from PIL import ImageDraw
cd = ImageDraw.Draw(curio_raw)
for y in range(int(ocy - 6), int(ocy + 7)):
    for x in range(int(ocx - 6), int(ocx + 7)):
        dx = x - ocx
        dy = y - ocy
        dist = (dx**2 + dy**2)**0.5
        if dist <= 4.5:
            spec = max(0.0, 1.0 - ((x - (ocx - 1.5))**2 + (y - (ocy - 1.5))**2)**0.5 / 5.0)
            shine = max(0.0, 1.0 - ((x - (ocx - 1.5))**2 + (y - (ocy - 1.5))**2)**0.5 / 2.0)**2
            r_sun = int(np.clip(255 * (0.8 + 0.2 * spec) + 40 * shine, 0, 255))
            g_sun = int(np.clip(208 * (0.8 + 0.2 * spec) + 40 * shine, 0, 255))
            b_sun = int(np.clip(40 * (0.6 + 0.4 * spec) + 80 * shine, 0, 255))
            curio_raw.putpixel((x, y), (r_sun, g_sun, b_sun, 255))

OUTLINE = (31, 26, 58, 255)
WHITE_SHINE = (255, 255, 255, 255)
SKY_BLUE_BASE = (56, 160, 255, 255)
SKY_BLUE_SHINE = (180, 225, 255, 255)
MINT_GREEN = (78, 216, 106, 255)
MINT_SHINE = (200, 255, 215, 255)
GOLD_SHINE = (255, 240, 120, 255)

cd.ellipse([int(ocx - 4.5), int(ocy - 4.5), int(ocx + 4.5), int(ocy + 4.5)], outline=OUTLINE, width=1)
cd.point((int(ocx - 1), int(ocy - 1)), fill=WHITE_SHINE)

# Planet 1: Sky Blue Enamel Planet bead on outer ring at (116, 55)
p1x, p1y = 116, 55
cd.ellipse([p1x - 3, p1y - 3, p1x + 3, p1y + 3], fill=SKY_BLUE_BASE, outline=OUTLINE)
cd.point((p1x - 1, p1y - 1), fill=SKY_BLUE_SHINE)

# Planet 2: Mint Green Planet bead on inner ring at (97, 65)
p2x, p2y = 97, 65
cd.ellipse([p2x - 2, p2y - 2, p2x + 2, p2y + 2], fill=MINT_GREEN, outline=OUTLINE)
cd.point((p2x, p2y), fill=MINT_SHINE)

# Tiny trailing starlight sparks around curio
for sx, sy in [(92, 52), (112, 70), (106, 44)]:
    cd.point((sx, sy), fill=GOLD_SHINE)

# PROPER OUTLINE: dilate mask from an immutable copy!
alpha_copy = np.array(curio_raw)[:, :, 3] > 80
outline_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(outline_img)
for y in range(1, H - 1):
    for x in range(1, W - 1):
        if not alpha_copy[y, x]:
            if alpha_copy[y-1, x] or alpha_copy[y+1, x] or alpha_copy[y, x-1] or alpha_copy[y, x+1]:
                od.point((x, y), fill=OUTLINE)

curio_clean = Image.alpha_composite(outline_img, curio_raw)
bb = curio_clean.getbbox()
print("Clean curio bbox:", bb)

arr = np.array(curio_clean)
alpha = arr[:, :, 3]
sub = alpha[bb[1]:bb[3], bb[0]:bb[2]]
for row in sub:
    line = "".join("#" if v > 20 else "." for v in row)
    print(line)
