from PIL import Image
import numpy as np

img = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/idle.png")
print("Macaque idle.png size:", img.size, "mode:", img.mode)
arr = np.array(img)
print("Alpha min/max:", int(arr[:,:,3].min()), int(arr[:,:,3].max()))
white = np.all(arr == [255, 255, 255, 255], axis=-1)
print("Pure white fully opaque pixels:", int(np.sum(white)))

# Also check macaque_battle.png
img_battle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/macaque_battle.png")
print("Macaque battle.png size:", img_battle.size, "mode:", img_battle.mode)

# Crop player from proof_07_battle_macaque.png
proof = Image.open("/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_02d07272/screenshots/proof_07_battle_macaque.png")
p_crop = proof.crop((50, 60, 360, 380))
p_crop.save("/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_02d07272/screenshots/macaque_player_zoom.png")
print("Saved /root/.hermes/kanban/boards/side-bravesoul/workspaces/t_02d07272/screenshots/macaque_player_zoom.png")
