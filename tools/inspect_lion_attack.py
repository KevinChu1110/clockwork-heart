import os
from PIL import Image

p = "game/assets/sprites/player/poses/lion/attack.png"
im = Image.open(p)
print("Lion attack pose size:", im.size, "bbox:", im.getbbox())
# crop torso and hands
# Lion attack bbox is (4, 9, 119, 126)
crop = im.crop((0, 0, 128, 128))
# save 4x magnified for inspection
crop_4x = crop.resize((512, 512), Image.Resampling.NEAREST)
crop_4x.save("/tmp/lion_attack_pose_4x.png")
print("Saved /tmp/lion_attack_pose_4x.png")
