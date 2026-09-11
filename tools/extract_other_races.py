import os
import subprocess

proof_dir = "/opt/side/bravesoul-game/proofs/combat_feel"
races = ["lion", "fox", "boar"]

for r in races:
    d = os.path.join(proof_dir, f"tmp_{r}")
    os.makedirs(d, exist_ok=True)
    mp4 = os.path.join(proof_dir, f"{r}_combat.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp4, f"{d}/frame_%03d.png"])
    print(f"Extracted {r} frames: {len(os.listdir(d))}")
