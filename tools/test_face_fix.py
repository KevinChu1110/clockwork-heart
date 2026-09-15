from PIL import Image
import numpy as np

idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/idle.png")
chassis = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png")

# Let's inspect the diff between idle and chassis
# In idle, let's look at the face region: x=40..80, y=25..60
arr_i = np.array(idle)
arr_c = np.array(chassis)

# Copy the face from idle to chassis where idle has the eyes, mouth, face details
# Let's see what pixels in idle face are:
# In idle, the face is roughly x: 42..75, y: 28..58
# Let's see what happens if we composite the idle face area into chassis
face_mask = np.zeros((128, 128), dtype=bool)
face_mask[28:58, 42:78] = True
# Only where idle is not fully transparent
face_mask &= (arr_i[:, :, 3] > 0)

arr_new = arr_c.copy()
# Replace face pixels with idle pixels
arr_new[face_mask] = arr_i[face_mask]

new_chassis = Image.fromarray(arr_new)
new_chassis.save("/opt/side/bravesoul-game/screenshots/test_new_chassis.png")

# Now composite with other 6 layers
layers = [
    "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/back_curio/curio_spring_tail.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/winding_key/key_classic_brass.png",
    "/opt/side/bravesoul-game/screenshots/test_new_chassis.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/head_unit/ear_macaque_coaxial.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/costume/costume_dawn_monk_tunic.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/optic_core/core_cyan_emerald.png",
    "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/weapon/wpn_spring_claws.png",
]

base = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
for lyr in layers:
    im = Image.open(lyr)
    base.alpha_composite(im)

base.save("/opt/side/bravesoul-game/screenshots/test_new_composite.png")
print("Saved test_new_composite.png")
