#!/usr/bin/env python3
from PIL import Image

im = Image.open('/opt/side/bravesoul-game/proofs/tortoise-i18n/proof_wardrobe_tortoise_en.png')
print("Image size:", im.size)

# Let's crop several horizontal slices of the left side (X: 200 to 500)
# In crop_wardrobe_cards (X: 220~920, Y: 150~600), we saw the preview of character was around X: 220~400
# So character stage is between X: 200 and X: 450!
# Where is the text below character?
c1 = im.crop((220, 480, 440, 600))
c1.save('/opt/side/bravesoul-game/proofs/tortoise-i18n/crops/crop_left_stage_bottom_en.png')
print("Saved crop_left_stage_bottom_en.png")
