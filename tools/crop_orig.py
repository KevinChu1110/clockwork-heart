from PIL import Image

img_orig = Image.open("/opt/side/bravesoul-game/proofs/battle-broken-i18n/proof_battle_broken_en.png")
crop = img_orig.crop((0, 0, 450, 150))
crop.save("/opt/side/bravesoul-game/proofs/qa_round38/crops/crop_orig_parent_en.png")
print("Original parent crop saved")
