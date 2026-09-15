import os
from PIL import Image

workdir = "/opt/side/bravesoul-game"

targets = [
    "game/assets/sprites/pack_a/vfx_drop_brass_gear.png",
    "game/assets/sprites/pack_a/vfx_drop_core_shard.png",
    "game/assets/sprites/pack_a/vfx_drop_spring_coil.png",
    "game/assets/sprites/pack_a/xiaobai_b02_cel.png",
    "game/assets/sprites/pack_a/v2/xiaobai_b02.png",
    "game/assets/sprites/pack_a/v2/xiaobai_d02.png",
    "game/assets/sprites/pack_a/v2/xiaobai_e03.png",
    "game/assets/sprites/pack_a/v2/paper_doll/oh_anim_strip.png",
    "game/assets/sprites/pack_a/v2/paper_doll/oh_ready_onehand.png",
    "game/assets/sprites/pack_a/v2/paper_doll/default_equips.png",
    "game/assets/sprites/pack_a/v2/paper_doll/oh_anim_strip_v2.png",
    "game/assets/sprites/pack_a/v2/paper_doll/explore_dismantle_anims.png",
    "game/assets/sprites/pack_a/v2/paper_doll/frames/oh_ready.png"
]

for t in targets:
    p = os.path.join(workdir, t)
    if os.path.exists(p):
        with Image.open(p) as img:
            print(f"{t}: format={img.format}, size={img.size}, mode={img.mode}")
