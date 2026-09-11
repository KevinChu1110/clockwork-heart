import os
from PIL import Image

races = ["fox", "boar", "macaque"]
for r in races:
    p = f"game/assets/sprites/player/poses/{r}/attack.png"
    im = Image.open(p)
    crop_4x = im.resize((512, 512), Image.Resampling.NEAREST)
    out_p = f"/tmp/{r}_attack_pose_4x.png"
    crop_4x.save(out_p)
    print(f"Saved {out_p}")
