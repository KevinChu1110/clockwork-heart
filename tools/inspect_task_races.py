import os
from PIL import Image

races = ["rabbit", "lion", "fox", "boar", "macaque"]
poses = ["attack", "hit", "skill", "recover", "telegraph", "idle"]
for r in races:
    for p in poses:
        if r == "rabbit" and p in ["attack", "idle"]:
            path = f"game/assets/sprites/player/poses/{p}.png"
        else:
            path = f"game/assets/sprites/player/poses/{r}/{p}.png"
        if os.path.exists(path):
            im = Image.open(path)
            bbox = im.getbbox()
            print(f"{r:8s} {p:10s}: size={im.size} bbox={bbox}")
