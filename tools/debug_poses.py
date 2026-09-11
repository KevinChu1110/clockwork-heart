import os
from PIL import Image

output_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox"
for f in ["idle.png", "telegraph.png", "attack.png", "recover.png", "skill.png", "hit.png"]:
    p = os.path.join(output_dir, f)
    im = Image.open(p)
    print(f"{f}: size={im.size}, bbox={im.getbbox()}, mode={im.mode}")
