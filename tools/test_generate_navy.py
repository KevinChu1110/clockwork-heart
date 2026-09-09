from PIL import Image
import colorsys

def make_midnight_navy_chassis(base_img):
    w, h = base_img.size
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    sp = base_img.load()
    op = out.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = sp[x, y]
            if a < 10:
                continue
            lum = int(0.299 * r + 0.587 * g + 0.114 * b)
            if lum < 50:
                op[x, y] = (31, 26, 58, a)  # Outline #1F1A3A
            elif lum < 85:
                # Mechanical joints, ball sockets, hinges: Antique warm bronze/brass
                op[x, y] = (int(r * 0.55 + 130 * 0.45), int(g * 0.55 + 95 * 0.45), int(b * 0.55 + 40 * 0.45), a)
            elif lum < 120:
                # Deep shadow enamel / plate recess
                f = (lum - 85) / 35.0
                op[x, y] = (int(22 + f * 12), int(30 + f * 16), int(55 + f * 25), a)
            elif lum < 180:
                # Mid-tone Midnight Navy Enamel
                f = (lum - 120) / 60.0
                op[x, y] = (int(34 + f * 26), int(46 + f * 34), int(80 + f * 50), a)
            else:
                # Specular edge highlights & enamel shine
                f = max(0.0, min(1.0, (lum - 180) / 75.0))
                op[x, y] = (int(60 + f * 45), int(80 + f * 55), int(130 + f * 80), a)
    return out

base = Image.open('game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold.png').convert('RGBA')
navy = make_midnight_navy_chassis(base)
print("Navy size:", navy.size, "bbox:", navy.getbbox())
diff_alpha = sum(1 for y in range(128) for x in range(128) if navy.getpixel((x, y))[3] != base.getpixel((x, y))[3])
print("Diff alpha vs gold:", diff_alpha)
