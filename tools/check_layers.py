from PIL import Image
import numpy as np

p1 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/proof_paperdoll_macaque_composite.png")
print("proof_paperdoll_macaque_composite size:", p1.size, p1.mode)

# Let's inspect the layers of macaque paperdoll
layers = [
    "game/assets/sprites/player/paperdoll/macaque/winding_key/key_classic_brass.png",
    "game/assets/sprites/player/paperdoll/macaque/back_curio/curio_spring_tail.png",
    "game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png",
    "game/assets/sprites/player/paperdoll/macaque/head_unit/ear_macaque_coaxial.png",
    "game/assets/sprites/player/paperdoll/macaque/costume/costume_dawn_monk_tunic.png",
    "game/assets/sprites/player/paperdoll/macaque/optic_core/core_cyan_emerald.png",
    "game/assets/sprites/player/paperdoll/macaque/weapon/wpn_spring_claws.png",
]
for lyr in layers:
    im = Image.open("/opt/side/bravesoul-game/" + lyr)
    arr = np.array(im)
    # count semi-transparent white pixels
    r, g, b, a = arr[:,:,0], arr[:,:,1], arr[:,:,2], arr[:,:,3]
    white_mask = (r > 200) & (g > 200) & (b > 200) & (a > 50)
    print(f"{lyr}: size={im.size}, white pixels={np.sum(white_mask)}")
