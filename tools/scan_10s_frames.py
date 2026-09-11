import os
import subprocess
from PIL import Image

proof_dir = "/opt/side/bravesoul-game/proofs/combat_feel"
tmp_dir = os.path.join(proof_dir, "tmp_10s")
os.makedirs(tmp_dir, exist_ok=True)

mp4 = os.path.join(proof_dir, "combat_10s_verified.mp4")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp4, f"{tmp_dir}/frame_%03d.png"])
frames = sorted([f for f in os.listdir(tmp_dir) if f.endswith(".png")])
print(f"Total extracted frames: {len(frames)}")

# 尋找傷害數字跳字與 BREAK 跳字的幀
# 傷害跳字顏色 Color(1.0, 0.4, 0.35) -> R高、G中、B中偏低
# BREAK 顏色 Color(1.0, 0.85, 0.15) -> 金黃色
hit_frames = []
break_frames = []
attack_frames = []

for fn in frames:
    p = os.path.join(tmp_dir, fn)
    im = Image.open(p)
    # 檢查敵方傷害跳字區域 (x: 750~1100, y: 100~350)
    crop_enemy = im.crop((750, 100, 1100, 350))
    pixels = crop_enemy.load()
    w, h = crop_enemy.size
    
    has_dmg = False
    has_brk = False
    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y][:3]
            # 傷害紅色特徵
            if r > 210 and 70 <= g <= 140 and 60 <= b <= 120:
                has_dmg = True
            # 金黃色 BREAK 特徵
            if r > 220 and g > 180 and b < 60:
                has_brk = True
    if has_dmg:
        hit_frames.append(fn)
    if has_brk:
        break_frames.append(fn)

print(f"Frames with Damage Float: {hit_frames}")
print(f"Frames with BREAK Float: {break_frames}")
