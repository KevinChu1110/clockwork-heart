from PIL import Image

def crop_and_zoom(p, out_p, box, scale=6):
    im = Image.open(p).convert('RGBA')
    cropped = im.crop(box)
    w, h = cropped.size
    zoomed = cropped.resize((cropped.width * scale, cropped.height * scale), Image.Resampling.NEAREST)
    zoomed.save(out_p)
    print(f"Saved zoomed crop to {out_p}")

crop_and_zoom('/tmp/test_repaired_ivory.png', '/tmp/repaired_ivory_head.png', (25, 15, 95, 75), scale=6)
crop_and_zoom('/tmp/test_repaired_ivory.png', '/tmp/repaired_ivory_body.png', (25, 60, 95, 125), scale=6)
