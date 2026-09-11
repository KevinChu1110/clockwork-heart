import os
from PIL import Image

races = ["rabbit", "lion", "fox", "boar"]
base_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/poses"
out_dir = "/opt/side/bravesoul-game/proofs/combat_feel"
os.makedirs(out_dir, exist_ok=True)

for r in races:
    if r == "rabbit":
        atk_p = f"{base_dir}/attack.png"
    else:
        atk_p = f"{base_dir}/{r}/attack.png"
    im = Image.open(atk_p)
    im.save(f"{out_dir}/{r}_attack_full.png")
    # 放大4倍以供檢視
    try:
        resample = Image.Resampling.NEAREST
    except AttributeError:
        resample = Image.NEAREST
    im_large = im.resize((im.width * 4, im.height * 4), resample)
    im_large.save(f"{out_dir}/{r}_attack_4x.png")
    print(f"Saved {r} attack full and 4x to {out_dir}")
