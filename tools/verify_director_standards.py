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
    120: "proof_f0120_rabbit_ready_dawn_blade.png",
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

# 6. 逐項查核五族代表格：零勝利結算畫面 (無「勝 利」、無「勝利！」)、武器持握與打擊效果
# 遵照總監二退指示：採方案 A 動作區間規範，兔族代表格改為 f0120（持劍備戰），實證銀刃長劍在手；
# 成片動作區間完整保留 f0116~f0130（拔刀→突進→命中），並在下方加驗 f0126 命中幀之受擊與跳字。
combat_samples = [
    ("Rabbit", "proof_f0120_rabbit_ready_dawn_blade.png", True),
    ("Lion", "proof_f0204_lion_knight_pike.png", False),
    ("Fox", "proof_f0282_fox_star_rod.png", False),
    ("Boar", "proof_f0354_boar_anvil_hammer.png", False),
    ("Macaque", "proof_f0433_macaque_hunt_claw.png", False),
]

print("\n>>> 查核五族代表格之零勝利結算狀態與武器/打擊效果 (第 19i 條):")
for rname, fname, is_ready_pose in combat_samples:
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
    
    if is_ready_pose:
        # 方案 A：兔族 f0120 為持劍備戰姿態，驗證晨光長劍（金屬刃+藍十字護手）在手
        rabbit_box = arr[800:1100, 300:600]
        metal_blade_px = np.sum((rabbit_box[:,:,0] > 180) & (rabbit_box[:,:,1] > 180) & (rabbit_box[:,:,2] > 180))
        blue_guard_px = np.sum((rabbit_box[:,:,2] > 140) & (rabbit_box[:,:,2] > rabbit_box[:,:,0] + 30))
        print(f"  [{rname}] 方案 A 持劍備戰格武器檢測: metal_blade_px={metal_blade_px}, blue_guard_px={blue_guard_px}")
        assert metal_blade_px > 500 and blue_guard_px > 500, f"[{rname}] Weapon entity (dawn_blade) not detected in rabbit hand!"
        assert yel_hit_px < 50, f"[{rname}] Enemy should not have golden hit ring in ready pose frame!"
    else:
        assert (red_hit_px > 200 or yel_hit_px > 200), f"[{rname}] No hit effect or damage float detected!"

# 7. 驗證兔族成片動作區間 (f0116~f0130) 之命中受擊幀 (f0126)
f126_arr = extracted_samples.get(126)
if f126_arr is None:
    # 從影片提取 frame 126
    f126_raw = subprocess.check_output([
        "ffmpeg", "-ss", "4.200", "-i", VIDEO_PATH, "-vframes", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"
    ])
    f126_arr = np.frombuffer(f126_raw, dtype=np.uint8).reshape((HEIGHT, WIDTH, 3))

f126_enemy_box = f126_arr[750:1150, 550:950]
f126_red_hit = np.sum((f126_enemy_box[:,:,0] > 190) & (f126_enemy_box[:,:,1] < 130) & (f126_enemy_box[:,:,2] < 130))
f126_yel_hit = np.sum((f126_enemy_box[:,:,0] > 200) & (f126_enemy_box[:,:,1] > 150) & (f126_enemy_box[:,:,2] < 100))
print(f"\n>>> 兔族成片動作區間命中受擊幀 (f0126) 查驗: red_hit_px={f126_red_hit}, yel_hit_px={f126_yel_hit}")
assert (f126_red_hit > 200 or f126_yel_hit > 200), "Rabbit combat sequence missing hit FX or damage float at frame 126!"

print("\n>>> 所有檢查項 100% 全部通過！符合總監驗收標準！")
