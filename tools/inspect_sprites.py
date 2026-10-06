from PIL import Image
import os

paths = [
    "/opt/side/bravesoul-game/game/assets/sprites/player/rabbit_idle.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/manta_battle.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/manta_battle_512.png",
]
for p in paths:
    if os.path.exists(p):
        im = Image.open(p)
        print(p, im.size, im.mode)
    else:
        print("Not found:", p)
