import os
from PIL import Image

fox_pd = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/fox"
layers = {
    "shadow": f"{fox_pd}/chassis/paint_fox_orange.png",
    "tail": f"{fox_pd}/back_curio/curio_fox_astral_tail.png",
    "key": f"{fox_pd}/winding_key/key_classic_brass.png",
    "chassis": f"{fox_pd}/chassis/paint_fox_orange.png",
    "costume": f"{fox_pd}/costume/costume_astral_observer.png",
    "core": f"{fox_pd}/optic_core/core_cyan_emerald.png",
    "head": f"{fox_pd}/head_unit/ear_fox_radar.png",
    "weapon": f"{fox_pd}/weapon/wpn_astral_staff.png",
}

for k, p in layers.items():
    if os.path.exists(p):
        im = Image.open(p)
        print(f"{k}: size={im.size}, bbox={im.getbbox()}")
    else:
        print(f"{k}: NOT FOUND at {p}")
