from PIL import Image

# Let's inspect the silver pixels for each race in idle.png and their coordinates
races = {
    "rabbit": {
        "file": "/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png",
        "weapon_name": "dawn_blade (刃身)",
        "box": (60, 70, 80, 96),
    },
    "lion": {
        "file": "/opt/side/bravesoul-game/game/assets/sprites/player/poses/lion/idle.png",
        "weapon_name": "knight_lance (槍杆)",
        "box": (38, 85, 55, 116),
    },
    "fox": {
        "file": "/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/idle.png",
        "weapon_name": "astral_staff (杖身)",
        "box": (35, 58, 48, 72),
    },
    "boar": {
        "file": "/opt/side/bravesoul-game/game/assets/sprites/player/poses/boar/idle.png",
        "weapon_name": "anvil_hammer (鎚頭)",
        "box": (38, 75, 55, 105), # let's check boar
    }
}

for race, data in races.items():
    im = Image.open(data["file"]).convert("RGBA")
    bx0, by0, bx1, by1 = data["box"]
    silver_pts = []
    for y in range(by0, by1 + 1):
        for x in range(bx0, bx1 + 1):
            r, g, b, a = im.getpixel((x, y))
            if a > 128 and r > 195 and g > 195 and b > 195 and abs(r - b) < 40:
                silver_pts.append((x, y, r, g, b))
    print(f"[{race}] {data['weapon_name']} in box {data['box']}: {len(silver_pts)} silver pixels in source")
    if silver_pts:
        ar = sum(p[2] for p in silver_pts) / len(silver_pts)
        ag = sum(p[3] for p in silver_pts) / len(silver_pts)
        ab = sum(p[4] for p in silver_pts) / len(silver_pts)
        print(f"  Source avg RGB: ({ar:.1f}, {ag:.1f}, {ab:.1f}), r-b={ar-ab:.1f}")
