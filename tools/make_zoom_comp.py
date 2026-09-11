from PIL import Image

def generate_zoom_comparison(mac_path, rab_path, out_path):
    rows = []
    for p, l in [(mac_path, 'MACAQUE'), (rab_path, 'RABBIT')]:
        im = Image.open(p).convert('RGBA')
        im = im.resize((im.width * 8, im.height * 8), Image.Resampling.NEAREST)
        rows.append((l, im))
        
    W = sum(i.width for _, i in rows) + 20
    H = max(i.height for _, i in rows)
    c = Image.new('RGBA', (W, H), (255, 0, 255, 255))
    x = 0
    for l, i in rows:
        c.paste(i, (x, 0), i)
        x += i.width + 20
        
    c.convert('RGB').save(out_path)
    print(f"✓ Saved {out_path} ({c.size})")

if __name__ == "__main__":
    generate_zoom_comparison(
        "/tmp/perfect_ivory_clean.png",
        "game/assets/sprites/player/paperdoll/rabbit/chassis/paint_ivory_stock.png",
        "/tmp/test_chassis_zoom_new.png"
    )
