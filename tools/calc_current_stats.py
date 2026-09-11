from PIL import Image

scale = 200.0 / 128.0
ox = 224.0
oy = 248.0 # 223.0 + 25.0

races = {
    "rabbit": {
        "file": "/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png",
        "screen": "/opt/side/bravesoul-game/proofs/combat_feel/rabbit_battle_idle.png",
        "weapon_name": "dawn_blade (刃身)",
        "box": (60, 70, 80, 96),
    },
    "lion": {
        "file": "/opt/side/bravesoul-game/game/assets/sprites/player/poses/lion/idle.png",
        "screen": "/opt/side/bravesoul-game/proofs/combat_feel/lion_battle_idle.png",
        "weapon_name": "knight_lance (槍杆)",
        "box": (38, 85, 55, 116),
    },
    "fox": {
        "file": "/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/idle.png",
        "screen": "/opt/side/bravesoul-game/proofs/combat_feel/fox_battle_idle.png",
        "weapon_name": "astral_staff (杖身)",
        "box": (35, 58, 48, 72),
    },
    "boar": {
        "file": "/opt/side/bravesoul-game/game/assets/sprites/player/poses/boar/idle.png",
        "screen": "/opt/side/bravesoul-game/proofs/combat_feel/boar_battle_idle.png",
        "weapon_name": "anvil_hammer (鎚頭)",
        "box": (38, 75, 55, 105),
    }
}

print("=== CURRENT NUMBERS ON EXISTING SCREENSHOTS (grade ON, sat=1.22) ===")
for race, data in races.items():
    im = Image.open(data["file"]).convert("RGBA")
    sc = Image.open(data["screen"]).convert("RGB")
    bx0, by0, bx1, by1 = data["box"]
    
    # Silver pixels in idle
    source_pts = []
    for y in range(by0, by1 + 1):
        for x in range(bx0, bx1 + 1):
            r, g, b, a = im.getpixel((x, y))
            if a > 128 and r > 195 and g > 195 and b > 195 and abs(r - b) < 40:
                source_pts.append((x, y))
    
    # Map to screen pixels:
    # Method 1: map center of each source pixel to screen
    silvers_c = 0
    browns_c = 0
    rgbs_c = []
    for x, y in source_pts:
        sx = int(ox + (x + 0.5) * scale)
        sy = int(oy + (y + 0.5) * scale)
        sr, sg, sb = sc.getpixel((sx, sy))
        rgbs_c.append((sr, sg, sb))
        if sr > 185 and sg > 185 and sb > 185 and abs(sr - sb) < 40:
            silvers_c += 1
        if sr - sb > 50:
            browns_c += 1
    
    n_c = len(source_pts)
    avg_r = sum(c[0] for c in rgbs_c) / n_c
    avg_g = sum(c[1] for c in rgbs_c) / n_c
    avg_b = sum(c[2] for c in rgbs_c) / n_c
    print(f"[{race}] {data['weapon_name']}: {n_c} sampled points")
    print(f"  Silver (>185, |r-b|<40): {silvers_c}/{n_c} ({silvers_c/n_c*100:.1f}%)")
    print(f"  Warm/Brown (r-b>50):   {browns_c}/{n_c} ({browns_c/n_c*100:.1f}%)")
    print(f"  Average Screen RGB:     ({avg_r:.1f}, {avg_g:.1f}, {avg_b:.1f}), r-b={avg_r-avg_b:.1f}")
