from PIL import Image
import numpy as np

b = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/macaque_battle.png")
c = b.crop((40, 25, 85, 65))
c.save("/opt/side/bravesoul-game/screenshots/macaque_battle_box.png")

arr = np.array(c)
alpha = arr[:,:,3]
ys, xs = np.where(alpha > 0)
print(f"macaque_battle: count={len(ys)}")
