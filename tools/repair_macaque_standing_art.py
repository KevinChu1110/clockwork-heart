#!/usr/bin/env python3
"""
修復靈爪猴官方全尺寸品牌立牌 (branding/char_macaque.png) 左側邊界切斷面
遵循 references/review.md 0-QA7, 0-QA9 與 t_bbe01af4 規範：
- 靈爪猴原圖左側手臂／機關護手／機械耳畫到畫布最邊緣，補 4:5 背景色時露出垂直切斷面
- 依 docs/art/spring_macaque_concept.png 母稿真跡與精密全局平移對齊 (dx=291, dy=-97)
- 透過光滑非線性空間映射將完整收尾（含同心圓轉軸耳部、機關護手轉折雙旋鈕、手部自然閉合輪廓線與金屬高光）
  完整收攏於原畫布邊界內 (x_core >= 14px)，左側邊界留有乾淨背景餘裕
- 邊緣過渡採微米級餘弦背景過渡，徹底消除邊界垂直接縫與色差條帶
- 修復後配合 tools/unify_race_cards_4_5.py 重產兩份 4:5 官方素材
"""

import os
from PIL import Image
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONCEPT_PATH = os.path.join(REPO_ROOT, "docs", "art", "spring_macaque_concept.png")
BRANDING_PATH = os.path.join(REPO_ROOT, "branding", "char_macaque.png")

def repair_macaque():
    concept = Image.open(CONCEPT_PATH)
    branding = Image.open(BRANDING_PATH)
    core = np.array(branding)[:, 272:1072, :].copy() # 800x1680
    h, w, c = core.shape

    # 概念稿縮放至 800x1680 (2x) 規格
    s2 = (206.0 / 305.0) * 2.0
    scaled_c2 = concept.resize(
        (int(round(concept.size[0] * s2)), int(round(concept.size[1] * s2))),
        Image.Resampling.LANCZOS
    )
    arr_sc2 = np.array(scaled_c2)

    bg_core = core[0, 0, :3].astype(float) # [235, 226, 209]
    bg_sc2 = arr_sc2[0, 0, :3].astype(float) # [244, 235, 206]
    color_shift = bg_core - bg_sc2

    dx = 291.0
    dy = -97.0

    # 非線性邊緣映射：將 x_sc2 in [242, 361] (包含母稿完整未裁切邊界) 光滑映射至 x_core in [14, 70]
    def map_x_core_to_sc2(x_core):
        if x_core >= 70:
            return x_core + dx
        if x_core < 14:
            return None
        t = (x_core - 14.0) / (70.0 - 14.0)
        return (1.0 - t)**2 * 242.0 + 2.0 * (1.0 - t) * t * 292.0 + t**2 * (70.0 + dx)

    test_core = core.copy().astype(float)

    # 步驟 1: 左側邊界背景平滑準備 (x=0..40 餘弦過渡至 bg_core)
    for y_core in range(h):
        orig_bg_ambient = core[y_core, 40, :3].astype(float)
        if np.linalg.norm(orig_bg_ambient - bg_core) > 40:
            orig_bg_ambient = bg_core
            
        for x_core in range(40):
            if x_core < 14:
                bg_val = bg_core
            else:
                t = (x_core - 14.0) / (40.0 - 14.0)
                blend = 0.5 * (1.0 - np.cos(t * np.pi))
                bg_val = (1.0 - blend) * bg_core + blend * orig_bg_ambient
            test_core[y_core, x_core] = bg_val

    # 步驟 2: 精準雙線性取樣並透過 Alpha 遮罩無縫合成未裁切真跡
    for y_core in range(h):
        y_sc2 = y_core + dy
        if 0 <= y_sc2 < scaled_c2.size[1]:
            for x_core in range(70):
                x_sc2 = map_x_core_to_sc2(x_core)
                if x_sc2 is not None:
                    ix = int(x_sc2)
                    iy = int(y_sc2)
                    fx = x_sc2 - ix
                    fy = y_sc2 - iy
                    
                    p00 = arr_sc2[iy, ix, :3].astype(float)
                    p10 = arr_sc2[iy, min(ix+1, arr_sc2.shape[1]-1), :3].astype(float)
                    p01 = arr_sc2[min(iy+1, arr_sc2.shape[0]-1), ix, :3].astype(float)
                    p11 = arr_sc2[min(iy+1, arr_sc2.shape[0]-1), min(ix+1, arr_sc2.shape[1]-1), :3].astype(float)
                    
                    sampled = (1-fx)*(1-fy)*p00 + fx*(1-fy)*p10 + (1-fx)*fy*p01 + fx*fy*p11
                    dist_bg = np.linalg.norm(sampled - bg_sc2)
                    
                    # 柔和抗鋸齒 Alpha 遮罩
                    if dist_bg <= 14.0:
                        alpha = 0.0
                    elif dist_bg >= 32.0:
                        alpha = 1.0
                    else:
                        t = (dist_bg - 14.0) / (32.0 - 14.0)
                        alpha = 3.0 * t**2 - 2.0 * t**3
                        
                    if alpha > 0.0:
                        adj_col = sampled + color_shift * (1.0 - 0.4 * alpha)
                        if x_core >= 55:
                            w_orig = (x_core - 55.0) / 15.0
                            char_col = (1.0 - w_orig) * adj_col + w_orig * core[y_core, x_core]
                        else:
                            char_col = adj_col
                            
                        test_core[y_core, x_core] = (1.0 - alpha) * test_core[y_core, x_core] + alpha * char_col

    repaired_core = np.clip(test_core, 0, 255).astype(np.uint8)

    # 寫回 branding/char_macaque.png 的 800x1680 核心區域
    full_arr = np.array(branding).copy()
    full_arr[:, 272:1072, :] = repaired_core

    repaired_branding = Image.fromarray(full_arr)
    repaired_branding.save(BRANDING_PATH, format="PNG")
    print(f"✓ 靈爪猴原圖左側收尾修復完成，已更新 {BRANDING_PATH}")

if __name__ == "__main__":
    repair_macaque()
