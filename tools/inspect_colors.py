from PIL import Image
from collections import Counter

for path in [
    'game/assets/sprites/player/paperdoll/lion/costume/costume_nutcracker_guard.png',
    'game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold.png',
    'game/assets/sprites/player/paperdoll/lion/chassis/paint_ivory_stock.png',
]:
    im = Image.open(path).convert('RGBA')
    w, h = im.size
    pixels = [im.getpixel((x, y)) for y in range(h) for x in range(w) if im.getpixel((x, y))[3] > 10]
    c = Counter(pixels)
    print(f"=== {path} ===")
    print(f"Top 10 colors:")
    for col, count in c.most_common(10):
        print(f"  {col}: {count}")
