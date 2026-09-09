from PIL import Image

def inspect_img(path):
    im = Image.open(path)
    w, h = im.size
    pixels = im.load()
    non_zero = sum(1 for y in range(h) for x in range(w) if pixels[x, y][3] > 0)
    print(path, im.size, im.mode)
    print('  opaque/semi pixels:', non_zero)
    print('  bbox:', im.getbbox())

inspect_img('game/assets/sprites/player/paperdoll/lion/costume/costume_nutcracker_guard.png')
inspect_img('game/assets/sprites/player/paperdoll/rabbit/costume/costume_steam_artisan.png')
inspect_img('game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold.png')
inspect_img('game/assets/sprites/player/paperdoll/lion/chassis/paint_ivory_stock.png')
