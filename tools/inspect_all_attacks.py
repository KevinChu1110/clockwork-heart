from PIL import Image

races = ["rabbit", "lion", "fox", "boar", "macaque"]
for r in races:
    if r == "rabbit":
        path = "/opt/side/bravesoul-game/game/assets/sprites/player/poses/attack.png"
    else:
        path = f"/opt/side/bravesoul-game/game/assets/sprites/player/poses/{r}/attack.png"
    im = Image.open(path).convert("RGBA")
    print(f"Race: {r}, attack size: {im.size}, bbox: {im.getbbox()}")
