import subprocess
from PIL import Image

with open("/tmp/attack_orig.png", "wb") as f:
    subprocess.run(["git", "show", "67101ed:game/assets/sprites/player/poses/macaque/attack.png"], stdout=f)

im_orig = Image.open("/tmp/attack_orig.png")
im_curr = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/attack.png")

print("Orig bbox:", im_orig.getbbox())
print("Curr bbox:", im_curr.getbbox())
