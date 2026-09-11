import os
from PIL import Image, ImageChops

frames = [f"proofs/combat_feel/tmp_10s/frame_{i:03d}.png" for i in range(1, 301)]
base = Image.open(frames[9]).crop((750, 100, 1100, 320))

diffs = []
for i, f in enumerate(frames):
    cur = Image.open(f).crop((750, 100, 1100, 320))
    d = ImageChops.difference(base, cur)
    stat = sum(list(d.convert("L").getdata()))
    if stat > 50000:
        diffs.append((i + 1, stat))

diffs.sort(key=lambda x: x[1], reverse=True)
print("Top 15 frames with enemy head diff:")
for frame_no, score in diffs[:15]:
    print(f"  Frame {frame_no:03d}: diff={score}")
