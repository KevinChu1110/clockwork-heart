from PIL import Image
import numpy as np

im = Image.open('/opt/side/bravesoul-game/proofs/t_bfd13f08/proof_01_bubble_charging_4h.png')
# Rabbit has white fur and red vest
# Let's crop around center x: 480 to 800, y: 100 to 450
crop = im.crop((480, 100, 800, 450))
crop.save('/opt/side/bravesoul-game/tools/crop_hero.png')
print("Saved crop_hero.png")
