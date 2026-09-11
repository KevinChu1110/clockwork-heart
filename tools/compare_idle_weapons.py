from PIL import Image
import os

repo = "/opt/side/bravesoul-game"
paperdoll = f"{repo}/game/assets/sprites/player/paperdoll"
weapons = {
    "rabbit": (f"{paperdoll}/rabbit/weapon/wpn_dawn_blade.png", f"{repo}/game/assets/sprites/player/poses/idle.png"),
    "lion": (f"{paperdoll}/lion/weapon/wpn_knight_lance.png", f"{repo}/game/assets/sprites/player/poses/lion/idle.png"),
    "fox": (f"{paperdoll}/fox/weapon/wpn_astral_staff.png", f"{repo}/game/assets/sprites/player/poses/fox/idle.png"),
    "boar": (f"{paperdoll}/boar/weapon/wpn_anvil_greathammer.png", f"{repo}/game/assets/sprites/player/poses/boar/idle.png"),
}

for race, (wpath, ipath) in weapons.items():
    wimg = Image.open(wpath).convert("RGBA")
    iimg = Image.open(ipath).convert("RGBA")
    print(f"=== {race} ===")
    print(f"  Weapon bbox: {wimg.getbbox()}")
    
    # Silver pixels in weapon image
    w_silver = []
    for y in range(wimg.height):
        for x in range(wimg.width):
            r, g, b, a = wimg.getpixel((x, y))
            if a > 128 and r > 195 and g > 195 and b > 195 and abs(r - b) < 40:
                w_silver.append((x, y, r, g, b))
    print(f"  Weapon file silver pixels: {len(w_silver)}")
    
    # In idle image within weapon bbox (or nearby)
    i_silver = []
    wbbox = wimg.getbbox()
    if wbbox:
        min_x, min_y, max_x, max_y = wbbox
        # Expand slightly
        for y in range(max(0, min_y - 2), min(iimg.height, max_y + 3)):
            for x in range(max(0, min_x - 2), min(iimg.width, max_x + 3)):
                r, g, b, a = iimg.getpixel((x, y))
                if a > 128 and r > 195 and g > 195 and b > 195 and abs(r - b) < 40:
                    i_silver.append((x, y, r, g, b))
    print(f"  Idle file silver pixels in weapon bbox: {len(i_silver)}")
    if i_silver:
        avg_r = sum(p[2] for p in i_silver) / len(i_silver)
        avg_g = sum(p[3] for p in i_silver) / len(i_silver)
        avg_b = sum(p[4] for p in i_silver) / len(i_silver)
        print(f"  Idle silver avg RGB: ({avg_r:.1f}, {avg_g:.1f}, {avg_b:.1f})")
