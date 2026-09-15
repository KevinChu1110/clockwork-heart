from PIL import Image
import numpy as np

proof = Image.open("/opt/side/bravesoul-game/screenshots/qa_round2/proof_07_battle_macaque.png")
# In 1280x720, where is player_body?
# PlayerBody is at x=176, y=148..600 (or somewhere on the left)
# Let's crop x: 150..400, y: 120..420
player_crop = proof.crop((150, 120, 400, 420))
player_crop.save("/opt/side/bravesoul-game/screenshots/captured_player_crop.png")
print("Saved captured_player_crop.png size:", player_crop.size)
