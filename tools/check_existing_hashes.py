import os
import hashlib
from PIL import Image

POSES_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox"

def get_hash(data):
    return hashlib.md5(data).hexdigest()

for p in ["idle", "telegraph", "attack", "recover", "skill", "hit"]:
    path = os.path.join(POSES_DIR, f"{p}.png")
    with open(path, "rb") as f:
        print(f"Existing {p:10s} md5: {get_hash(f.read())}")
