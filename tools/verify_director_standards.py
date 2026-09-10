#!/usr/bin/env python3
import os
import subprocess
from PIL import Image
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VIDEO_PATH = os.path.join(ROOT, "web/media/shorts/mk_shorts_five_races_combat_18s.mp4")
SHEET_PATH = os.path.join(ROOT, "docs/marketing/shots/mk_shorts_five_races_combat_18s_contact_sheet.png")
SHOTS_DIR = os.path.join(ROOT, "docs/marketing/shots")

print("=================================================================")
print("=== 總監級嚴格全自動查驗腳本 (對齊 review.md 第 19f, 19i 條) ===")
print("=================================================================")

WIDTH = 1080
HEIGHT = 1920
FRAME_BYTES = WIDTH * HEIGHT * 3

print(">>> 正在透過 ffmpeg rawvideo 串流快速讀取 540 幀 (零磁碟 I/O)...")
cmd = [
    "ffmpeg", "-loglevel", "error",
    "-i", VIDEO_PATH,
    "-f", "rawvideo",
    "-pix_fmt", "rgb24",
    "-"
]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=FRAME_BYTES*4)

frames = []
prev_frame = None
diffs = []
frame_idx = 0

sample_targets = {
    45: "proof_f0045_shot1_macro.png",
    126: "proof_f0126_rabbit_dawn_blade.png",
    204: "proof_f0204_lion_knight_pike.png",
    282: "proof_f0282_fox_star_rod.png",
    354: "proof_f0354_boar_anvil_hammer.png",
    433: "proof_f0433_macaque_hunt_claw.png",
    504: "proof_f0504_shot7_title.png",
}
extracted_samples = {}

while True:
    raw = proc.stdout.read(FRAME_BYTES)
    if len(raw) < FRAME_BYTES:
        break
    arr = np.frombuffer(raw, dtype=np.uint8).reshape((HEIGHT, WIDTH, 3))
    
    if prev_frame is not None:
        d = np.mean(np.abs(arr.astype(np.float32) - prev_frame.astype(np.float32)))
        diffs.append(d)
    
    if frame_idx in sample_targets:
        extracted_samples[frame_idx] = arr.copy()
        
    prev_frame = arr
    frame_idx += 1

proc.stdout.close()
proc.wait()

print(f"串流讀取完成：共 {frame_idx} 幀（預期 540 幀）")
assert frame_idx == 540, f"Frame count mismatch: {frame_idx} != 540"

# 2. 逐幀相鄰差量測 (Adjacent Frame Difference)
mean_diff = np.mean(diffs)
max_diff = np.max(diffs)
print(f">>> 全片相鄰幀平均差: mean = {mean_diff:.2f}, max = {max_diff:.2f}")
assert mean_diff > 2.0, f"Video too static: mean diff {mean_diff:.2f} <= 2.0"

# 3. 檢查片尾 sec 16-17 (幀 480..520) 相鄰幀差
diffs_16_17 = diffs[480:520]
sec16_17_mean = np.mean(diffs_16_17)
sec16_17_min = np.min(diffs_16_17)
print(f">>> 片尾 sec 16-17 相鄰幀差: mean = {sec16_17_mean:.2f}, min = {sec16_17_min:.2f}")
assert sec16_17_mean > 1.0, f"Sec 16-17 too static: {sec16_17_mean:.2f} <= 1.0 (原退稿為 0.22)"

# 4. 查驗 6 個真實鏡頭剪點
cut_points = [90, 165, 240, 315, 390, 465]
for cp in cut_points:
    d = diffs[cp - 1]
    print(f"  剪點 frame {cp:04d} 前後切換差: {d:.2f}")
    assert d > 15.0, f"Cut point at {cp} is not sharp: diff {d:.2f}"

# 5. 逐一比對抽樣代表圖與影片同源幀的像素差 (0.0000 驗證)
print("\n>>> 比對抽格圖與影片實際畫格像素一致性 (第 19f 條同源查核):")
for f_idx, proof_fname in sample_targets.items():
    proof_p = os.path.join(SHOTS_DIR, proof_fname)
    assert os.path.exists(proof_p), f"Missing proof: {proof_p}"
    
    img_proof = np.array(Image.open(proof_p).convert("RGB"))
    img_v = extracted_samples[f_idx]
    p_diff = np.mean(np.abs(img_proof.astype(np.float32) - img_v.astype(np.float32)))
    print(f"  {proof_fname} vs frame {f_idx:04d}: pixel diff = {p_diff:.4f}")
    # 由於 ffmpeg -ss 精確取樣與逐幀解出的時間戳對齊，驗證像素差極小 (小於 0.05)
    assert p_diff < 0.05, f"Proof {proof_fname} does not match video frame {f_idx} (diff={p_diff})!"

# 6. 逐項查核五族代表格：零勝利結算畫面 (無「勝 利」、無「勝利！」)、有命中特效或傷害跳字
combat_samples = [
    ("Rabbit", "proof_f0126_rabbit_dawn_blade.png"),
    ("Lion", "proof_f0204_lion_knight_pike.png"),
    ("Fox", "proof_f0282_fox_star_rod.png"),
    ("Boar", "proof_f0354_boar_anvil_hammer.png"),
    ("Macaque", "proof_f0433_macaque_hunt_claw.png"),
]

print("\n>>> 查核五族代表格之打擊效果與零勝利結算狀態 (第 19i 條):")
for rname, fname in combat_samples:
    p = os.path.join(SHOTS_DIR, fname)
    arr = np.array(Image.open(p).convert("RGB"))
    
    # 檢查中央區域是否含有中央「勝 利」金字
    center_box = arr[800:1100, 400:680]
    gold_banner_px = np.sum((center_box[:,:,0] > 230) & (center_box[:,:,1] > 200) & (center_box[:,:,2] < 70))
    
    # 檢查戰鬥日誌 (左下方) 是否含有綠色「勝利！」
    log_box = arr[1100:1300, 100:500]
    green_victory_px = np.sum((log_box[:,:,1] > 220) & (log_box[:,:,0] < 120) & (log_box[:,:,2] < 120))
    
    # 檢查敵方區域傷害跳字與特效
    enemy_box = arr[750:1150, 550:950]
    red_hit_px = np.sum((enemy_box[:,:,0] > 190) & (enemy_box[:,:,1] < 130) & (enemy_box[:,:,2] < 130))
    yel_hit_px = np.sum((enemy_box[:,:,0] > 200) & (enemy_box[:,:,1] > 150) & (enemy_box[:,:,2] < 100))
    
    print(f"  [{rname}] gold_banner_px={gold_banner_px}, green_victory_px={green_victory_px}, red_hit_px={red_hit_px}, yel_hit_px={yel_hit_px}")
    assert gold_banner_px < 50, f"[{rname}] Detected victory banner in combat frame!"
    assert green_victory_px < 50, f"[{rname}] Detected victory log in combat frame!"
    assert (red_hit_px > 200 or yel_hit_px > 200), f"[{rname}] No hit effect or damage float detected!"

print("\n>>> 所有檢查項 100% 全部通過！符合總監驗收標準！")
