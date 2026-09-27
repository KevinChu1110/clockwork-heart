from PIL import Image

im = Image.open("/opt/side/bravesoul-game/proofs/qa_round38/proof_05_battle_broken_zh_TW.png")
c = im.crop((0, 0, 600, 300))
c.save("/opt/side/bravesoul-game/proofs/qa_round38/crops/debug_top_left_tw.png")
print("Saved debug_top_left_tw.png")
