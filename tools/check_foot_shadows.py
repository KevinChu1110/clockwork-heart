from PIL import Image
import os

for path in [
    "/opt/side/bravesoul-game/game/assets/sprites/player/poses/attack.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/poses/rabbit/idle.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit/composite_final_master.png"
]:
    if os.path.exists(path):
        im = Image.open(path).convert("RGBA")
        w, h = im.size
        print(path, w, h)
        found = 0
        for y in range(h - 1, -1, -1):
            hits = [im.getpixel((x, y)) for x in range(w) if im.getpixel((x, y))[3] > 10]
            if hits:
                dark_hits = [c for c in hits if c[0] < 50 and c[1] < 50 and c[2] < 50]
                print(f"  y={y}: total_opaque={len(hits)}, dark={len(dark_hits)}")
                found += 1
                if found > 10:
                    break
