from PIL import Image
import numpy as np

# Load individual layers of macaque paperdoll
layer_paths = [
    ("chassis", "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png"),
    ("head_unit", "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/head_unit/ear_macaque_coaxial.png"),
    ("optic_core", "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/optic_core/core_cyan_emerald.png"),
    ("costume", "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/costume/costume_dawn_monk_tunic.png"),
    ("back_curio", "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/back_curio/curio_spring_tail.png"),
    ("winding_key", "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/winding_key/key_classic_brass.png"),
    ("weapon", "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/weapon/wpn_spring_claws.png"),
    ("proof_composite", "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/proof_paperdoll_macaque_composite.png"),
    ("macaque_battle", "/opt/side/bravesoul-game/game/assets/sprites/player/macaque_battle.png"),
    ("macaque_idle", "/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/idle.png"),
]

for name, path in layer_paths:
    try:
        im = Image.open(path)
        arr = np.array(im)
        # check face area: for 128x128 images, face is roughly y=25..65, x=40..85
        if arr.shape[0] == 128 and arr.shape[1] == 128:
            face = arr[25:65, 40:85]
            # check pixels where r>220, g>220, b>220, a>30
            white = (face[:,:,0] > 200) & (face[:,:,1] > 200) & (face[:,:,2] > 200) & (face[:,:,3] > 30)
            print(f"{name:15s} (128x128) face white pixels: {np.sum(white)}")
        else:
            print(f"{name:15s} size={im.size}")
    except Exception as e:
        print(f"{name:15s} ERROR: {e}")
