#!/usr/bin/env python3
import os
import subprocess
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TMP_DIR = "/root/tmp_workspace"
PROOF_DIR = f"{ROOT}/proofs/combat_feel"
os.makedirs(PROOF_DIR, exist_ok=True)

RACES = {
    "rabbit": {"name": "白金兔 晨光長劍", "wpn": "dawn_blade", "atk_time": "00:00:04.10"},
    "lion": {"name": "烈鬃獅 皇家長槍", "wpn": "knight_pike", "atk_time": "00:00:04.10"},
    "fox": {"name": "靈尾狐 星盤秘術法杖", "wpn": "star_rod", "atk_time": "00:00:04.10"},
    "boar": {"name": "鋼牙豕 鍛爐鐵砧戰鎚", "wpn": "anvil_hammer", "atk_time": "00:00:04.30"},
    "macaque": {"name": "靈爪猴 機關發條靈爪", "wpn": "hunt_claw", "atk_time": "00:00:02.75"},
}

for race, info in RACES.items():
    raw_mp4 = f"{TMP_DIR}/raw_{race}_16x9.mp4"
    if not os.path.exists(raw_mp4):
        print(f"Missing {raw_mp4}")
        continue
    
    # 抽取攻擊揮擊前衝瞬間的 1280x720 原生畫面 (確認武器手持與揮舞姿態)
    ss_time = info["atk_time"]
    raw_frame_path = f"{TMP_DIR}/{race}_raw_attack_frame.png"
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-ss", ss_time, "-i", raw_mp4,
        "-vframes", "1", raw_frame_path
    ], check=True)

    im = Image.open(raw_frame_path)
    # PlayerSlot 在 1280x720 畫面左側攻擊位移區約 x: 160~520, y: 180~520
    crop_box = (160, 180, 520, 520)
    cropped = im.crop(crop_box)
    
    # 放大 3 倍維持細節
    resample = getattr(Image, "Resampling", Image).NEAREST # type: ignore
    large = cropped.resize((cropped.width * 3, cropped.height * 3), resample)
    out_crop = f"{PROOF_DIR}/{race}_weapon_crop.png"
    large.save(out_crop)
    print(f"[{race.upper()}] Cropped {info['name']} (from attack swing at {ss_time}) -> {out_crop} ({large.size})")
