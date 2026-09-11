import os
from PIL import Image

repo = "/opt/side/bravesoul-game"
paperdoll = f"{repo}/game/assets/sprites/player/paperdoll"

for race in ["rabbit", "lion", "fox", "boar", "macaque"]:
    wpn_dir = f"{paperdoll}/{race}/weapon"
    if os.path.exists(wpn_dir):
        for f in sorted(os.listdir(wpn_dir)):
            if f.endswith(".png") and not f.endswith(".import"):
                p = os.path.join(wpn_dir, f)
                im = Image.open(p)
                print(f"{race} weapon ({f}): bbox={im.getbbox()} size={im.size}")
