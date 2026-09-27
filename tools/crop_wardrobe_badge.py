#!/usr/bin/env python3
from PIL import Image

img = Image.open('/opt/side/bravesoul-game/proofs/fawn-i18n/proof_wardrobe_fawn_en.png')
# Dialog is at X: 265, Y: 70, W: 750, H: 580
# Left stage is X: 285~510, badge is at bottom of stage (around Y: 380~470)
crop = img.crop((280, 380, 520, 480))
crop.save('/opt/side/bravesoul-game/proofs/fawn-i18n/crops/crop_wardrobe_badge_en.png')

for loc in ['zh_TW', 'en', 'ja']:
    im = Image.open(f'/opt/side/bravesoul-game/proofs/fawn-i18n/proof_wardrobe_fawn_{loc}.png')
    c = im.crop((280, 380, 520, 480))
    c.save(f'/opt/side/bravesoul-game/proofs/fawn-i18n/crops/crop_wardrobe_badge_{loc}.png')
    print(f'Saved badge crop for {loc}')
