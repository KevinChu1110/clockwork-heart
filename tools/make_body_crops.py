from PIL import Image

def crop_and_zoom(p, out_p, box, scale=6):
    im = Image.open(p).convert('RGBA')
    cropped = im.crop(box)
    w, h = im.size
    zoomed = cropped.resize((cropped.width * scale, cropped.height * scale), Image.Resampling.NEAREST)
    zoomed.save(out_p)
    print(f"Saved zoomed crop to {out_p}")

crop_and_zoom('game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png', '/tmp/mac_ivory_body.png', (25, 60, 95, 125), scale=6)
