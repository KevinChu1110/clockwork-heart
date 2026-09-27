#!/usr/bin/env python3
from PIL import Image

im = Image.open('/opt/side/bravesoul-game/proofs/fawn-i18n/proof_wardrobe_fawn_en.png')
w, h = im.size
print(f'Size: {w}x{h}')

# Let's crop the entire left side of the dialog (X: 265 to 550, Y: 70 to 600)
# and save it as debug_left_stage.png
stage = im.crop((265, 70, 550, 620))
stage.save('/opt/side/bravesoul-game/proofs/fawn-i18n/crops/debug_left_stage.png')
print('Saved debug_left_stage.png')
