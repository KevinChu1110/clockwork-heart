from PIL import Image
import numpy as np

img = Image.open('proofs/shop-sku-i18n/crops/crop_shop_en_cards.png').convert('RGB')
# Let's crop just the button of card 1 or card 2
# In crop_shop_en_cards (750x260):
# Card 2 is roughly x in [260, 480], button is at the bottom y in [190, 250]
btn2 = img.crop((270, 195, 470, 250))
btn2.save('/tmp/btn2.png')

# Let's save a 10x zoom of the letter 'M' in Mock Purchase
# Let's find where 'M' is inside btn2
arr = np.array(btn2)
print("btn2 size:", btn2.size)

# Zoom btn2 4x and save
btn2_4x = btn2.resize((btn2.width * 4, btn2.height * 4), Image.Resampling.NEAREST)
btn2_4x.save('/tmp/btn2_4x.png')
print("Saved /tmp/btn2_4x.png")
