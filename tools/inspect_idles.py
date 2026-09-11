import os
from PIL import Image

races = ["rabbit", "lion", "fox", "boar"]
base_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/poses"
out_dir = "/opt/side/bravesoul-game/proofs/combat_feel"

for r in races:
    if r == "rabbit":
        idle_p = f"{base_dir}/idle.png"
    else:
        idle_p = f"{base_dir}/{r}/idle.png"
    im = Image.open(idle_p)
    try:
        resample = Image.Resampling.NEAREST
    except AttributeError:
        resample = Image.NEAREST
    im_large = im.resize((im.width * 4, im.height * 4), resample)
    im_large.save(f"{out_dir}/{r}_idle_4x.png")
    print(f"Saved {r} idle 4x")
