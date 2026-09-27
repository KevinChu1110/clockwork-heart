from PIL import Image

im = Image.open("/opt/side/bravesoul-game/proofs/t_f9b106b5/proof_wardrobe_seahorse.png")
# Stage panel: x=280..545, y=110..670
stage_crop = im.crop((280, 110, 545, 670))
stage_crop.save("/opt/side/bravesoul-game/proofs/t_f9b106b5/proof_crop_wardrobe_seahorse.png")
print("Saved accurate stage crop:", stage_crop.size)

# Cards panel: x=545..1000, y=110..670
cards_crop = im.crop((545, 110, 1000, 670))
cards_crop.save("/opt/side/bravesoul-game/proofs/t_f9b106b5/proof_crop_wardrobe_seahorse_cards.png")
print("Saved accurate cards crop:", cards_crop.size)
