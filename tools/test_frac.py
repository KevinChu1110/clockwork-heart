from PIL import Image

def sim_content_bottom_frac(path: str, scan_start_117: bool) -> float:
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    last = int(h * 0.88)
    found = False
    scan_start = 117 if (scan_start_117 and 120 <= h <= 136) else h - 1
    for y in range(scan_start, -1, -1):
        hit = False
        x = 0
        while x < w:
            p = im.getpixel((x, y))
            if isinstance(p, tuple) and p[3] / 255.0 > 0.28:
                hit = True
                break
            x += 3
        if hit:
            last = y
            found = True
            break
    frac = 0.90
    if found and h > 0:
        frac = max(0.58, min(0.94, (float(last) + 1.0) / float(h) - 0.03))
    print(f"{path}: scan_start={scan_start}, last={last}, frac={frac:.4f}")
    return frac

sim_content_bottom_frac("game/assets/sprites/player/poses/attack.png", False)
sim_content_bottom_frac("game/assets/sprites/player/poses/attack.png", True)
sim_content_bottom_frac("game/assets/sprites/player/poses/idle.png", False)
