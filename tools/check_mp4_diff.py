import os
import glob
import subprocess
import numpy as np
from PIL import Image

for mp4 in sorted(glob.glob("/opt/side/bravesoul-game/proofs/combat_feel/*_combat.mp4")):
    tmp = "/tmp/test_frames"
    os.system(f"rm -rf {tmp} && mkdir -p {tmp}")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-i", mp4, f"{tmp}/f_%04d.png"])
    frames = sorted(glob.glob(f"{tmp}/f_*.png"))
    if not frames:
        print(f"{mp4}: no frames")
        continue
    f0 = np.array(Image.open(frames[0]).convert("RGB"), dtype=np.float32)
    max_d = 0.0
    for f in frames[1:]:
        fi = np.array(Image.open(f).convert("RGB"), dtype=np.float32)
        d = np.abs(f0 - fi).mean()
        if d > max_d:
            max_d = d
    print(f"{mp4}: frames={len(frames)}, max_diff={max_d:.2f}")
