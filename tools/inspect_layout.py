from PIL import Image

img = Image.open('proofs/shop-sku-i18n/proof_shop_en.png')
print("Proof size:", img.size)

# The dialog is centered in 1280x720.
# Let's save a thumbnail or inspect sections
# Let's find where the 3 item cards are.
# In shop_dialog.gd, what are the positions?
