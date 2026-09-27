from PIL import Image, ImageChops

im1 = Image.open("/opt/side/bravesoul-game/proofs/qa_round38/proof_06_battle_broken_en.png")
im2 = Image.open("/opt/side/bravesoul-game/proofs/battle-broken-i18n/proof_battle_broken_en.png")

diff = ImageChops.difference(im1, im2)
bbox = diff.getbbox()
print("Diff bbox between qa38 and parent en:", bbox)
