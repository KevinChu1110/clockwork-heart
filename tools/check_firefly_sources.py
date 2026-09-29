import os
from PIL import Image

repo = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_e4a76321"
assets = [
    "game/assets/sprites/player/poses/firefly/idle.png",
    "game/assets/sprites/player/poses/firefly/idle_512.png",
    "game/assets/sprites/player/poses/firefly/attack.png",
    "game/assets/sprites/player/poses/firefly/attack_512.png",
    "game/assets/sprites/player/firefly_battle.png",
    "game/assets/sprites/player/firefly_battle_512.png",
    "game/assets/sprites/player/paperdoll/firefly/chassis/chassis_firefly_emerald_tinplate_default.png",
    "game/assets/sprites/player/paperdoll/firefly/chassis/chassis_firefly_emerald_tinplate_default_512.png",
    "game/assets/sprites/player/paperdoll/firefly/head_unit/head_firefly_brass_antenna_cowl.png",
    "game/assets/sprites/player/paperdoll/firefly/head_unit/head_firefly_brass_antenna_cowl_512.png",
    "game/assets/sprites/player/paperdoll/firefly/optic_core/face_firefly_dual_lantern_quartz_eyes.png",
    "game/assets/sprites/player/paperdoll/firefly/optic_core/face_firefly_dual_lantern_quartz_eyes_512.png",
    "game/assets/sprites/player/paperdoll/firefly/costume/costume_firefly_vine_harness_cuirass.png",
    "game/assets/sprites/player/paperdoll/firefly/costume/costume_firefly_vine_harness_cuirass_512.png",
    "game/assets/sprites/player/paperdoll/firefly/winding_key/key_firefly_floral_gear_brass.png",
    "game/assets/sprites/player/paperdoll/firefly/winding_key/key_firefly_floral_gear_brass_512.png",
    "game/assets/sprites/player/paperdoll/firefly/weapon/weapon_firefly_luminescent_vine_staff.png",
    "game/assets/sprites/player/paperdoll/firefly/weapon/weapon_firefly_luminescent_vine_staff_512.png",
    "game/assets/sprites/player/paperdoll/firefly/back_curio/curio_firefly_luminescent_resin_abdomen.png",
    "game/assets/sprites/player/paperdoll/firefly/back_curio/curio_firefly_luminescent_resin_abdomen_512.png"
]

for p in assets:
    f = f"{repo}/{p}"
    if os.path.exists(f):
        im = Image.open(f)
        print(f"EXISTS: {p} size={im.size} mode={im.mode} bbox={im.getbbox()}")
    else:
        print(f"MISSING: {p}")
