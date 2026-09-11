import os
from PIL import Image
import numpy as np

poses = ["idle", "attack", "skill", "hit", "telegraph", "recover"]

# Let's inspect the player sprite in f78
f78 = Image.open("/opt/side/bravesoul-game/proofs/macaque_frames/f_0078.png").convert("RGBA")
# Let's find player body in f78:
# In PlayerSlot, where is the TextureRect?
# Let's compare the texture inside player_f_0078 against each of the 6 pose files
for p in poses:
    pose_img = Image.open(f"/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/{p}.png").convert("RGBA")
    print(f"Pose: {p}, size: {pose_img.size}")
