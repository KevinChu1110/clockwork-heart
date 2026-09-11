import subprocess
from PIL import Image

with open("/tmp/attack_base.png", "wb") as f:
    subprocess.run(["git", "show", "67101ed:game/assets/sprites/player/poses/macaque/attack.png"], stdout=f)

base = Image.open("/tmp/attack_base.png")
print("Base attack size:", base.size)
print("Base attack bbox:", base.getbbox())

# Let's see what is on base attack around the punching hand (x: 75..105, y: 48..70)
# We can crop and save it
crop_base = base.crop((75, 48, 105, 70))
crop_base.save("/tmp/base_fist.png")
print("Base fist saved to /tmp/base_fist.png, bbox:", crop_base.getbbox())
