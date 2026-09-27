from PIL import Image
import numpy as np

img = Image.open('proofs/shop-sku-i18n/crops/crop_shop_en_cards.png').convert('RGB')
arr = np.array(img)

# Look for dark pixels (text) in middle card (x from 250 to 500)
# Card 2 is roughly x in [250, 500]
print("Image size:", img.size)

# Let's save a vertical strip of card 2 to see where everything is
card2 = img.crop((245, 0, 505, 260))
card2.save('/tmp/card2_full.png')
print("Saved /tmp/card2_full.png size:", card2.size)
