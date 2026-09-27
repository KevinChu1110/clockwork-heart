from PIL import Image

im = Image.open("/opt/side/bravesoul-game/proofs/qa_round38/proof_06_battle_broken_en.png")

# Let's inspect columns from x=0 to x=60 at y=50 (where PlayerHPLabel is)
# Let's find where non-transparent/non-background pixels start on the left
# Also let's inspect the entire left margin:
print("Image width, height:", im.size)

# Crop the left margin specifically: x: 0..100, y: 0..150
crop_margin = im.crop((0, 0, 150, 150))
crop_margin.save("/opt/side/bravesoul-game/proofs/qa_round38/crops/check_margin_en.png")

crop_margin_tw = Image.open("/opt/side/bravesoul-game/proofs/qa_round38/proof_05_battle_broken_zh_TW.png").crop((0, 0, 150, 150))
crop_margin_tw.save("/opt/side/bravesoul-game/proofs/qa_round38/crops/check_margin_tw.png")

print("Margin crops saved")
