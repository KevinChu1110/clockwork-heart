from PIL import Image

img = Image.open("/opt/side/bravesoul-game/proofs/qa_round38/proof_06_battle_broken_en.png")
print("Size:", img.size)

# Let's inspect where the player HUD is located in both images
img_tw = Image.open("/opt/side/bravesoul-game/proofs/qa_round38/proof_05_battle_broken_zh_TW.png")
print("TW size:", img_tw.size)
