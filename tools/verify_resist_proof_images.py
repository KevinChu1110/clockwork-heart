from PIL import Image
import os

proof_dir = "/opt/side/bravesoul-game/proofs/resist-combat-hud"
for fname in sorted(os.listdir(proof_dir)):
    if not fname.endswith(".png"):
        continue
    fpath = os.path.join(proof_dir, fname)
    im = Image.open(fpath)
    print(f"{fname}: {im.size}, mode={im.mode}")
