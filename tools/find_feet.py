from PIL import Image

def find_feet(path: str) -> None:
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    print(f"=== {path} ({w}x{h}) ===")
    # Find player bounds
    min_x, max_x, min_y, max_y = w, 0, h, 0
    for y in range(h):
        for x in range(w):
            p = im.getpixel((x, y))
            if isinstance(p, tuple) and p[3] > 100:
                # check if it is within player area (x roughly 100 to 600)
                if 100 <= x <= 600:
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)
    print(f"Player bounds: x=[{min_x}, {max_x}], y=[{min_y}, {max_y}]")

find_feet("screenshots/proof_battle_full_screen.png")
find_feet("screenshots/proof_battle_equipped_royal_parade.png")
find_feet("screenshots/proof_battle_attack_sword.png")
find_feet("proofs/combat_feel/boar_battle_idle.png")
