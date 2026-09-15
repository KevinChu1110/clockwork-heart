from PIL import Image
import numpy as np

battle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/macaque_battle.png")
ivory = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png")

arr_b = np.array(battle)
arr_i = np.array(ivory)

# Let's inspect where battle has head pixels:
# Head in battle is x: 26..84, y: 14..64.
# Notice: In battle, is the winding key attached to the head?
# Let's check where winding key is:
key = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/winding_key/key_classic_brass.png")
arr_k = np.array(key)

# The face region where ivory was smeared is specifically the face panel:
# From y: 22 to 64, x: 28 to 82.
# In this region, battle has the clean ivory face with eyes, mouth, nose, helmet!
# Does battle have any winding key pixels in x: 28..82, y: 22..64?
# In battle, the winding key is around x: 80..105, y: 28..52.
# So for x < 80, y between 15 and 64, battle has ONLY the head and face!
mask = np.zeros((128, 128), dtype=bool)
for y in range(15, 65):
    for x in range(26, 80):
        if arr_b[y, x, 3] > 0:
            mask[y, x] = True

# Also ensure we don't pick up winding key
mask &= (arr_k[:, :, 3] == 0)

arr_new_ivory = arr_i.copy()
arr_new_ivory[mask] = arr_b[mask]

new_ivory = Image.fromarray(arr_new_ivory)
new_ivory.save("/opt/side/bravesoul-game/screenshots/new_paint_ivory_stock.png")

# Now let's test compositing with all 7 layers!
layers = [
    "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/back_curio/curio_spring_tail.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/winding_key/key_classic_brass.png",
    "/opt/side/bravesoul-game/screenshots/new_paint_ivory_stock.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/head_unit/ear_macaque_coaxial.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/costume/costume_dawn_monk_tunic.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/optic_core/core_cyan_emerald.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/weapon/wpn_spring_claws.png",
]

comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
for lyr in layers:
    im = Image.open(lyr)
    comp.alpha_composite(im)

comp.save("/opt/side/bravesoul-game/screenshots/comp_with_new_ivory.png")
print("Saved comp_with_new_ivory.png")
