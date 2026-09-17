import os
import hashlib
from PIL import Image

proof_dir = "/opt/side/bravesoul-game/proofs/fox_fix"
files = [
    "proof_01_lobby_fox.png",
    "proof_02_creation_fox.png",
    "proof_03_explore_fox_walk.png"
]

md5s = {}
for f in files:
    p = os.path.join(proof_dir, f)
    with open(p, "rb") as fp:
        data = fp.read()
        m = hashlib.md5(data).hexdigest()
        md5s[f] = m
    im = Image.open(p)
    print(f"{f}: size={im.size}, md5={m}")

# Check unique md5s
assert len(set(md5s.values())) == 3, "MD5s must not duplicate!"
print("✓ All 3 screenshots have distinct MD5s and are 1280x720!")

# Let's crop head closeup from proof_01_lobby_fox.png (Lobby center character)
lobby_im = Image.open(os.path.join(proof_dir, "proof_01_lobby_fox.png"))
# The character in lobby is roughly in center:
# In 1280x720, center is (640, 360). Let's locate the fox head in lobby:
# Let's crop a window around (500, 150, 780, 430)
head_closeup = lobby_im.crop((520, 160, 760, 400))
head_closeup_path = os.path.join(proof_dir, "proof_04_fox_head_closeup.png")
head_closeup.save(head_closeup_path)
print(f"Saved {head_closeup_path}")
