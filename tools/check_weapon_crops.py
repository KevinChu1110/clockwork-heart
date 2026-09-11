from PIL import Image
import os

proof_dir = "/opt/side/bravesoul-game/proofs/combat_feel"
for f in sorted(os.listdir(proof_dir)):
    if "weapon" in f and f.endswith(".png"):
        p = os.path.join(proof_dir, f)
        im = Image.open(p)
        print(f"{f}: size={im.size}")
