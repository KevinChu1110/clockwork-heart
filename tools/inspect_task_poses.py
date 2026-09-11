import os
from PIL import Image

races = ["rabbit", "lion", "fox", "boar", "macaque"]
base_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/poses"

poses = ["idle", "attack", "skill", "hit", "recover", "telegraph"]

for r in races:
    print(f"=== {r} ===")
    for p in poses:
        if r == "rabbit":
            fpath = f"{base_dir}/{p}.png"
        else:
            fpath = f"{base_dir}/{r}/{p}.png"
        if os.path.exists(fpath):
            im = Image.open(fpath)
            print(f"  {p}: exists, size={im.size}, mode={im.mode}, bbox={im.getbbox()}")
        else:
            print(f"  {p}: MISSING ({fpath})")
