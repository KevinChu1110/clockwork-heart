#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

# 載入野豬各部件 512
chassis = Image.open(f"{BOAR_DIR}/chassis/paint_brass_gold_512.png").convert("RGBA")
head = Image.open(f"{BOAR_DIR}/head_unit/ear_boar_rivet_cowl_brass_512.png").convert("RGBA")
costume_iron = Image.open(f"{BOAR_DIR}/costume/costume_viking_ironclad_512.png").convert("RGBA")
costume_harn = Image.open(f"{BOAR_DIR}/costume/costume_viking_harness_512.png").convert("RGBA")
weapon = Image.open(f"{BOAR_DIR}/weapon/wpn_anvil_greathammer_512.png").convert("RGBA")
core = Image.open(f"{BOAR_DIR}/optic_core/core_cyan_emerald_512.png").convert("RGBA")
comp_128 = Image.open(f"{BOAR_DIR}/proof_paperdoll_boar_composite.png").convert("RGBA")

print("Chassis 512 bbox:", chassis.getbbox())
print("Head 512 bbox:", head.getbbox())
print("Costume Ironclad 512 bbox:", costume_iron.getbbox())
print("Costume Harness 512 bbox:", costume_harn.getbbox())
print("Weapon 512 bbox:", weapon.getbbox())
print("Core 512 bbox:", core.getbbox())

# 分析 Head: 底部交接處與眼睛位置
h_arr = np.array(head)
# 找到 head 的最底部 y
head_ys, head_xs = np.where(h_arr[:, :, 3] > 20)
print(f"Head Y range: {head_ys.min()} .. {head_ys.max()}, X range: {head_xs.min()} .. {head_xs.max()}")
# 底部中心 x
bottom_y = head_ys.max()
bottom_xs = head_xs[head_ys == bottom_y]
print(f"Head bottom Y={bottom_y}, X center={np.mean(bottom_xs):.1f}")

# 分析 Chassis: 最頂部 y
c_arr = np.array(chassis)
c_ys, c_xs = np.where(c_arr[:, :, 3] > 20)
print(f"Chassis Y range: {c_ys.min()} .. {c_ys.max()}, X range: {c_xs.min()} .. {c_xs.max()}")
top_y = c_ys.min()
top_xs = c_xs[c_ys == top_y]
print(f"Chassis top Y={top_y}, X center={np.mean(top_xs):.1f}")

# 分析 Core (胸前核心):
core_arr = np.array(core)
core_ys, core_xs = np.where(core_arr[:, :, 3] > 20)
print(f"Core Y center={np.mean(core_ys):.1f}, X center={np.mean(core_xs):.1f}")

# 分析 Weapon: 握持手部 hand 錨點位置
# 戰錘的柄在哪裡？
w_arr = np.array(weapon)
w_ys, w_xs = np.where(w_arr[:, :, 3] > 20)
print(f"Weapon Y range: {w_ys.min()} .. {w_ys.max()}, X range: {w_xs.min()} .. {w_xs.max()}")

# 檢查 128 合成圖中的各部位比例對應到 512
# 在 128 中，composite bbox 是 (18, 9, 111, 126)
# 乘 4 對應到 512 是 (72, 36, 444, 504)
