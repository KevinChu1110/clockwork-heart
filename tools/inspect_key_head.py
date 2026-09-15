from PIL import Image
import numpy as np

key = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/winding_key/key_classic_brass.png")
arr = np.array(key)
c = key.crop((20, 20, 55, 50))
c.save("/opt/side/bravesoul-game/screenshots/key_face_box.png")

# Also check head
head = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/head_unit/ear_macaque_coaxial.png")
c_head = head.crop((20, 20, 55, 50))
c_head.save("/opt/side/bravesoul-game/screenshots/head_face_box.png")

print("Saved key_face_box.png and head_face_box.png")
