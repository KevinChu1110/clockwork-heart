from PIL import Image

def analyze(path: str) -> None:
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    print(f"=== {path} ===")
    for y in range(0, h, 20):
        dark_count = 0
        for x in range(200, 600):
            p = im.getpixel((x, y))
            if isinstance(p, tuple):
                r, g, b = p[0], p[1], p[2]
                if r < 40 and g < 40 and b < 40:
                    dark_count += 1
        if dark_count > 10:
            print(f"y={y}: dark_count={dark_count}")

analyze("proofs/combat_feel/boar_battle_idle.png")
analyze("screenshots/proof_battle_full_screen.png")
