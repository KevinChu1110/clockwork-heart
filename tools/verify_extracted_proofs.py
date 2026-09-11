import subprocess
import numpy as np
from PIL import Image

mp4 = "/opt/side/bravesoul-game/proofs/combat_feel/macaque_combat.mp4"

# Extract exact frames using ffmpeg
pairs = [
    (10, "/opt/side/bravesoul-game/proofs/combat_feel/macaque_real_01_idle_f0010.png"),
    (78, "/opt/side/bravesoul-game/proofs/combat_feel/macaque_real_02_attack_f0078.png"),
    (81, "/opt/side/bravesoul-game/proofs/combat_feel/macaque_real_03_damage_f0081.png"),
    (85, "/opt/side/bravesoul-game/proofs/combat_feel/macaque_real_04_break_f0085.png"),
]

for frame_idx, png_path in pairs:
    # Extract frame directly to png_path
    # Note: ffmpeg select=eq(n\,X) where n is 0-indexed or 1-indexed.
    # In ffmpeg select filter, n starts at 0. So frame 10 (1-based) is n=9.
    # Let's extract frame using select=eq(n\,{})
    n_val = frame_idx - 1
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", mp4,
        "-vf", f"select=eq(n\\,{n_val})", "-vframes", "1", png_path
    ], check=True)
    
    # Also verify by extracting all frames and comparing
    ref_path = f"/tmp/macaque_all_frames/f_{frame_idx:04d}.png"
    im1 = np.array(Image.open(png_path).convert("RGB"), dtype=np.float32)
    im2 = np.array(Image.open(ref_path).convert("RGB"), dtype=np.float32)
    diff = np.abs(im1 - im2).mean()
    print(f"Frame {frame_idx:03d} -> {png_path}: diff vs video frame = {diff:.4f}")
