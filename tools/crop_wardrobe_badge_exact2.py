#!/usr/bin/env python3
from PIL import Image

for loc in ['zh_TW', 'en', 'ja']:
    im = Image.open(f'/opt/side/bravesoul-game/proofs/fawn-i18n/proof_wardrobe_fawn_{loc}.png')
    c = im.crop((265, 580, 520, 660))
    c.save(f'/opt/side/bravesoul-game/proofs/fawn-i18n/crops/crop_wardrobe_badge_{loc}.png')
    print(f'Saved badge crop for {loc}')
