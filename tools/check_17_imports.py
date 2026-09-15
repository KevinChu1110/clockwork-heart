import os

workdir = "/opt/side/bravesoul-game"

targets = [
    "game/assets/sprites/s8_smoke/b02_combat.png.import",
    "game/assets/sprites/s8_smoke/e03_explore.png.import",
    "game/assets/sprites/s8_smoke/d02_dismantle.png.import",
    "game/assets/sprites/pack_a/vfx_drop_brass_gear.png.import",
    "game/assets/sprites/pack_a/vfx_drop_spring_coil.png.import",
    "game/assets/sprites/pack_a/xiaobai_b02_cel.png.import",
    "game/assets/sprites/pack_a/vfx_drop_core_shard.png.import",
    "game/assets/sprites/pack_a/v2/xiaobai_b02.png.import",
    "game/assets/sprites/pack_a/v2/xiaobai_d02.png.import",
    "game/assets/sprites/pack_a/v2/xiaobai_e03.png.import",
    "game/assets/sprites/pack_a/v2/paper_doll/oh_anim_strip.png.import",
    "game/assets/sprites/pack_a/v2/paper_doll/oh_ready_onehand.png.import",
    "game/assets/sprites/pack_a/v2/paper_doll/default_equips.png.import",
    "game/assets/sprites/pack_a/v2/paper_doll/oh_anim_strip_v2.png.import",
    "game/assets/sprites/pack_a/v2/paper_doll/explore_dismantle_anims.png.import",
    "game/assets/sprites/pack_a/v2/paper_doll/frames/oh_ready.png.import",
    "game/assets/sprites/maps/temple_lobby_bg.png.import"
]

for t in targets:
    p = os.path.join(workdir, t)
    if os.path.exists(p):
        print(f"=== {t} ===")
        with open(p, "r", encoding="utf-8") as f:
            print(f.read().strip())
        print()
