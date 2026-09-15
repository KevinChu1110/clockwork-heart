from PIL import Image
import numpy as np

layers = [
    "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/back_curio/curio_spring_tail.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/winding_key/key_classic_brass.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/head_unit/ear_macaque_coaxial.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/costume/costume_dawn_monk_tunic.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/optic_core/core_cyan_emerald.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/weapon/wpn_spring_claws.png",
]

base = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
for lyr in layers:
    im = Image.open(lyr)
    base.alpha_composite(im)

base.save("/opt/side/bravesoul-game/screenshots/test_macaque_composite.png")
print("Saved test_macaque_composite.png")
