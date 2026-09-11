from PIL import Image
import os

repo = "/opt/side/bravesoul-game"
races = {
    "rabbit": f"{repo}/game/assets/sprites/player/poses/idle.png",
    "lion": f"{repo}/game/assets/sprites/player/poses/lion/idle.png",
    "fox": f"{repo}/game/assets/sprites/player/poses/fox/idle.png",
    "boar": f"{repo}/game/assets/sprites/player/poses/boar/idle.png",
}

for race, path in races.items():
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    silver_coords = []
    for y in range(h):
        for x in range(w):
            r, g, b, a = img.getpixel((x, y))
            if a > 128 and r > 195 and g > 195 and b > 195 and abs(r - b) < 40:
                silver_coords.append((x, y, r, g, b))
    print(f"=== {race} ({w}x{h}) ===")
    print(f"Total silver pixels (r,g,b>195, |r-b|<40): {len(silver_coords)}")
    # Where are they spatially?
    xs = [p[0] for p in silver_coords]
    ys = [p[1] for p in silver_coords]
    print(f"X: {min(xs)}-{max(xs)}, Y: {min(ys)}-{max(ys)}")
