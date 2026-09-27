from PIL import Image

img_tw = Image.open("/opt/side/bravesoul-game/proofs/qa_round38/proof_05_battle_broken_zh_TW.png")
img_en = Image.open("/opt/side/bravesoul-game/proofs/qa_round38/proof_06_battle_broken_en.png")

# Crop player HUD (x: 0..450, y: 0..150)
crop_tw = img_tw.crop((0, 0, 450, 150))
crop_en = img_en.crop((0, 0, 450, 150))
crop_tw.save("/opt/side/bravesoul-game/proofs/qa_round38/crops/crop_player_hud_zh_TW.png")
crop_en.save("/opt/side/bravesoul-game/proofs/qa_round38/crops/crop_player_hud_en.png")

# Crop boss top HUD (x: 800..1280, y: 0..150)
crop_boss_tw = img_tw.crop((800, 0, 1280, 150))
crop_boss_en = img_en.crop((800, 0, 1280, 150))
crop_boss_tw.save("/opt/side/bravesoul-game/proofs/qa_round38/crops/crop_boss_top_zh_TW.png")
crop_boss_en.save("/opt/side/bravesoul-game/proofs/qa_round38/crops/crop_boss_top_en.png")
print("Crops saved successfully")
