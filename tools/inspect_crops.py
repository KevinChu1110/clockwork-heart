from PIL import Image

im = Image.open('/opt/side/bravesoul-game/proofs/t_bfd13f08/proof_01_bubble_charging_4h.png')
# crop (700, 80, 950, 200)
crop = im.crop((700, 80, 950, 200))
crop.save('/opt/side/bravesoul-game/tools/crop_top.png')

# also crop (700, 280, 950, 400)
crop2 = im.crop((700, 280, 950, 400))
crop2.save('/opt/side/bravesoul-game/tools/crop_mid.png')

print("Saved crops.")
