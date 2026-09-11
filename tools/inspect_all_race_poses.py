import os
from PIL import Image, ImageChops

ROOT = os.path.abspath(".")
POSES = {
    "rabbit": {
        "idle": f"{ROOT}/game/assets/sprites/player/poses/idle.png",
        "attack": f"{ROOT}/game/assets/sprites/player/poses/attack.png",
    },
    "macaque": {
        "idle": f"{ROOT}/game/assets/sprites/player/poses/macaque/idle.png",
        "attack": f"{ROOT}/game/assets/sprites/player/poses/macaque/attack.png",
    },
    "lion": {
        "idle": f"{ROOT}/game/assets/sprites/player/poses/lion/idle.png",
        "attack": f"{ROOT}/game/assets/sprites/player/poses/lion/attack.png",
    },
    "boar": {
        "idle": f"{ROOT}/game/assets/sprites/player/poses/boar/idle.png",
        "attack": f"{ROOT}/game/assets/sprites/player/poses/boar/attack.png",
    },
    "fox": {
        "idle": f"{ROOT}/game/assets/sprites/player/poses/fox/idle.png",
        "attack": f"{ROOT}/game/assets/sprites/player/poses/fox/attack.png",
    },
}

for race, p in POSES.items():
    im_idle = Image.open(p["idle"]).convert("RGBA")
    im_atk = Image.open(p["attack"]).convert("RGBA")
    diff = ImageChops.difference(im_idle, im_atk)
    diff_px = sum(1 for px in diff.split()[-1].tobytes() if px > 0)
    raw_diff = sum(1 for px in diff.convert("L").tobytes() if px > 15)
    print(f"[{race.upper()}]")
    print(f"  idle size={im_idle.size}, bbox={im_idle.getbbox()}")
    print(f"  attack size={im_atk.size}, bbox={im_atk.getbbox()}")
    print(f"  alpha diff={diff_px} px, visual diff (>15)={raw_diff} px")
