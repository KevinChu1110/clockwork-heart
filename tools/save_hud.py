from PIL import Image

# Let's crop the actual top-left HUD with plenty of context: x: 0..400, y: 0..200
im = Image.open("/opt/side/bravesoul-game/proofs/qa_round38/proof_05_battle_broken_zh_TW.png")
c = im.crop((0, 0, 400, 200))
c.save("/opt/side/bravesoul-game/proofs/qa_round38/crops/actual_full_player_hud.png")
print("Saved actual_full_player_hud.png")
