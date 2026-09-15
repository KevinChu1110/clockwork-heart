from PIL import Image
import numpy as np

layers = [
    ("tail", "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/back_curio/curio_spring_tail.png"),
    ("key", "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/winding_key/key_classic_brass.png"),
    ("chassis", "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png"),
    ("head", "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/head_unit/ear_macaque_coaxial.png"),
    ("costume", "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/costume/costume_dawn_monk_tunic.png"),
    ("optic", "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/optic_core/core_cyan_emerald.png"),
    ("weapon", "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/weapon/wpn_spring_claws.png"),
]

for name, p in layers:
    im = Image.open(p)
    crop = im.crop((40, 25, 85, 65))
    crop.save(f"/opt/side/bravesoul-game/screenshots/box_{name}.png")
    arr = np.array(crop)
    alpha = arr[:,:,3]
    print(f"{name}: non-transparent pixels in face box: {np.sum(alpha > 0)}")
