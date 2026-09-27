from PIL import Image, ImageDraw
import numpy as np

W, H = 128, 128
kcx, kcy = 88.0, 34.0
r_outer = 15.0
r_mid = 10.5
r_inner = 6.0
r_hub = 3.0

key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
kd = ImageDraw.Draw(key_img)

OUTLINE = (31, 26, 58, 255)
GOLD_PRIMARY = (255, 208, 40, 255)
WHITE_SHINE = (255, 255, 255, 255)
GOLD_SHINE = (255, 240, 120, 255)

# Key shaft entering spine socket at (64, 64) up to (88, 34)
for t in np.linspace(0.0, 1.0, 45):
    sx = 64.0 + t * 24.0
    sy = 64.0 - t * 30.0
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            if dx**2 + dy**2 <= 4:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                r_s = int(np.clip(212 + 35 * spec, 0, 255))
                g_s = int(np.clip(160 + 30 * spec, 0, 255))
                b_s = int(np.clip(23 + 45 * spec, 0, 255))
                key_img.putpixel((int(sx + dx), int(sy + dy)), (r_s, g_s, b_s, 255))

kd.ellipse([60, 60, 68, 68], fill=(120, 90, 20, 255), outline=OUTLINE)
kd.ellipse([61, 61, 67, 67], fill=(212, 160, 23, 255))

for y in range(int(kcy - r_outer - 3), int(kcy + r_outer + 4)):
    for x in range(int(kcx - r_outer - 3), int(kcx + r_outer + 4)):
        dx = x - kcx
        dy = y - kcy
        dist = (dx**2 + dy**2)**0.5

        is_ring1 = (dist >= 12.8 and dist <= 15.2)
        is_ring2 = (dist >= 8.8 and dist <= 11.2)
        is_ring3 = (dist >= 4.8 and dist <= 6.8)
        is_hub = (dist <= 3.2)
        spoke_dist = abs(abs(dx) - abs(dy)) / 1.414
        is_spoke = (spoke_dist <= 1.2 and dist <= 14.5)

        if is_ring1 or is_ring2 or is_ring3 or is_hub or is_spoke:
            spec = max(0.0, 1.0 - ((x - (kcx - 4))**2 + (y - (kcy - 4))**2)**0.5 / 14.0)
            shine = max(0.0, 1.0 - ((x - (kcx - 5))**2 + (y - (kcy - 5))**2)**0.5 / 5.0)**2

            if is_ring1 and dx > 0 and dy < 0:
                r_k = int(np.clip(255 * (0.85 + 0.25 * spec) + 30 * shine, 0, 255))
                g_k = int(np.clip(208 * (0.85 + 0.25 * spec) + 40 * shine, 0, 255))
                b_k = int(np.clip(40 * (0.8 + 0.3 * spec) + 60 * shine, 0, 255))
            elif is_ring2 and dx < 0 and dy > 0:
                r_k = int(np.clip(180 * (0.85 + 0.25 * spec) + 50 * shine, 0, 255))
                g_k = int(np.clip(210 * (0.85 + 0.25 * spec) + 40 * shine, 0, 255))
                b_k = int(np.clip(255 * (0.85 + 0.25 * spec) + 30 * shine, 0, 255))
            else:
                r_k = int(np.clip(212 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                g_k = int(np.clip(160 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                b_k = int(np.clip(23 * (0.8 + 0.3 * spec) + 70 * shine, 0, 255))
            key_img.putpixel((x, y), (r_k, g_k, b_k, 255))

kd.ellipse([int(kcx - r_outer), int(kcy - r_outer), int(kcx + r_outer), int(kcy + r_outer)], outline=OUTLINE, width=1)
kd.ellipse([int(kcx - r_mid), int(kcy - r_mid), int(kcx + r_mid), int(kcy + r_mid)], outline=OUTLINE, width=1)
kd.ellipse([int(kcx - r_inner), int(kcy - r_inner), int(kcx + r_inner), int(kcy + r_inner)], outline=OUTLINE, width=1)
kd.ellipse([int(kcx - r_hub), int(kcy - r_hub), int(kcx + r_hub), int(kcy + r_hub)], fill=GOLD_PRIMARY, outline=OUTLINE)
kd.point((int(kcx - 1), int(kcy - 1)), fill=WHITE_SHINE)

for deg in [0, 90, 180, 270]:
    rad = np.radians(deg)
    bx = int(round(kcx + 14.0 * np.cos(rad)))
    by = int(round(kcy + 14.0 * np.sin(rad)))
    kd.ellipse([bx - 1, by - 1, bx + 1, by + 1], fill=GOLD_SHINE, outline=OUTLINE)

bb = key_img.getbbox()
print("Key bbox without extra outline loop:", bb)
arr = np.array(key_img)
sub = arr[17:52, 70:106]
for y, row in enumerate(sub):
    line = "".join("#" if row[x, 3] > 50 else "." for x in range(len(row)))
    print(f"{y+17:2d}: {line}")
