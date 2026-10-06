import os
import shutil

src = "/opt/side/bravesoul-game/game/assets/sprites/maps/battle_ruins_pixel.png"
dst1 = "/opt/side/bravesoul-game/game/assets/sprites/battle/battle_ruins_pixel.png"
dst2 = "/opt/side/bravesoul-game/game/assets/sprites/maps/stone_path_ruins_bg.png"

os.makedirs("/opt/side/bravesoul-game/game/assets/sprites/battle", exist_ok=True)
if os.path.exists(src):
    shutil.copy2(src, dst1)
    shutil.copy2(src, dst2)
    os.remove(src)
    print("Moved battle_ruins_pixel.png out of maps/ to battle/ and stone_path_ruins_bg.png")
else:
    print("Source file not found")
