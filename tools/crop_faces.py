from PIL import Image
import numpy as np

chassis = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png")
idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/idle.png")
battle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/macaque_battle.png")

# Let's save crops of face
c_crop = chassis.crop((40, 25, 85, 65))
c_crop.save("/opt/side/bravesoul-game/screenshots/chassis_face.png")

i_crop = idle.crop((40, 25, 85, 65))
i_crop.save("/opt/side/bravesoul-game/screenshots/idle_face.png")

b_crop = battle.crop((40, 25, 85, 65))
b_crop.save("/opt/side/bravesoul-game/screenshots/battle_face.png")

print("Saved crops")
