from PIL import Image, ImageChops
import os

p1 = "/opt/side/bravesoul-game/proofs/proof_battle_polish_bandit.png"
p2 = "/opt/side/bravesoul-game/proofs/proof_battle_polish_leo.png"
if not os.path.exists(p1):
    p1 = "/opt/side/bravesoul-game/screenshots/proof_battle_polish_bandit.png"
    p2 = "/opt/side/bravesoul-game/screenshots/proof_battle_polish_leo.png"

if os.path.exists(p1) and os.path.exists(p2):
    im1 = Image.open(p1)
    im2 = Image.open(p2)
    diff = ImageChops.difference(im1, im2)
    print("Polish bandit vs leo diff bbox:", diff.getbbox())
else:
    print("Files not found: ", p1, p2)
