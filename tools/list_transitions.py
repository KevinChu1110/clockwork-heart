import os
from PIL import Image, ImageChops

proof_dir = "/opt/side/bravesoul-game/proofs/combat_feel"
tmp_dir = os.path.join(proof_dir, "tmp_10s")

f1 = Image.open(os.path.join(tmp_dir, "frame_001.png"))
unique_frames = []
last_im = f1

for i in range(2, 301):
    cur = Image.open(os.path.join(tmp_dir, f"frame_{i:03d}.png"))
    d = ImageChops.difference(last_im, cur)
    if d.getbbox():
        unique_frames.append(i)
        last_im = cur

print(f"Total frame transitions found: {len(unique_frames)}")
print(f"Transition frame numbers: {unique_frames[:20]}")
