from PIL import Image

def crop_and_zoom(p, out_p, box, scale=8):
    im = Image.open(p).convert('RGBA')
    cropped = im.crop(box)
    w, h = cropped.size
    zoomed = cropped.resize((w * scale, h * scale), Image.Resampling.NEAREST)
    zoomed.save(out_p)
    print(f"Saved zoomed crop to {out_p}")

crop_and_zoom('game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png', '/tmp/mac_ivory_head.png', (25, 15, 95, 75), scale=6)
crop_and_zoom('game/assets/sprites/player/paperdoll/macaque/chassis/paint_bamboo_bronze.png', '/tmp/mac_bronze_head.png', (25, 15, 95, 75), scale=6)
crop_and_zoom('game/assets/sprites/player/paperdoll/rabbit/chassis/paint_ivory_stock.png', '/tmp/rab_ivory_head.png', (35, 30, 95, 90), scale=6)
