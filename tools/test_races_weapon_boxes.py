from PIL import Image

races = {
    "rabbit": {
        "idle": "/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png",
        "screen": "/opt/side/bravesoul-game/proofs/combat_feel/rabbit_battle_idle.png",
        # blade: x in [58, 80], y in [75, 96]
        "weapon_box": (58, 75, 80, 96),
        "part_name": "blade (刃身)"
    },
    "lion": {
        "idle": "/opt/side/bravesoul-game/game/assets/sprites/player/poses/lion/idle.png",
        "screen": "/opt/side/bravesoul-game/proofs/combat_feel/lion_battle_idle.png",
        # spear shaft / tip: where is the spear in lion idle?
        # let's find all silver in lion idle and check bounding boxes
        "weapon_box": (20, 10, 40, 120),
        "part_name": "spear shaft (槍杆)"
    },
    "fox": {
        "idle": "/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/idle.png",
        "screen": "/opt/side/bravesoul-game/proofs/combat_feel/fox_battle_idle.png",
        # staff: where is the staff in fox idle?
        "weapon_box": (80, 35, 115, 125),
        "part_name": "staff (杖身)"
    },
    "boar": {
        "idle": "/opt/side/bravesoul-game/game/assets/sprites/player/poses/boar/idle.png",
        "screen": "/opt/side/bravesoul-game/proofs/combat_feel/boar_battle_idle.png",
        # hammer head / shaft:
        "weapon_box": (18, 55, 60, 125),
        "part_name": "hammer head (鎚頭)"
    },
}

for rname, info in races.items():
    idle = Image.open(info["idle"]).convert("RGBA")
    print(f"=== {rname} ===")
    silvers = []
    for y in range(idle.height):
        for x in range(idle.width):
            r, g, b, a = idle.getpixel((x, y))
            if a > 128 and r > 195 and g > 195 and b > 195 and abs(r - b) < 40:
                silvers.append((x, y, r, g, b))
    
    # Filter by weapon box if any
    box = info["weapon_box"]
    wpn_silvers = [p for p in silvers if box[0] <= p[0] <= box[2] and box[1] <= p[1] <= box[3]]
    print(f"  Total silver in idle: {len(silvers)}")
    print(f"  Silver in {info['part_name']} box {box}: {len(wpn_silvers)}")
    if not wpn_silvers:
        print("  All silver locations:")
        for p in silvers[:20]:
            print(f"    ({p[0]}, {p[1]}): RGB({p[2]},{p[3]},{p[4]})")
