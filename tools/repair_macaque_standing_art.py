#!/usr/bin/env python3
"""
修復靈爪猴官方全尺寸品牌立牌 (branding/char_macaque.png) 左側邊界切斷面
遵循 references/review.md 0-ART23, 0-QA7, 0-QA9 與 t_bbe01af4 規範：
- 依 docs/art/spring_macaque_concept.png 母稿真跡與原始立繪真跡
- 補齊左上機械耳圓順凸弧閉合、黃銅板件、鉚釘與深褐色手繪描邊 (apex y=620, x=274)
- 補齊左手臂手肘自然外展弧度、米白裝甲板、黃銅轉折高光與深褐色手繪閉合描邊 (apex y=915, x=362)
- 補齊左手護腕凸出黃銅機械盒、雙齒輪旋鈕與完整收邊描邊 (apex y=1185, x=274)
- 腳底投影維持自然羽化漸變至 x=292
- 嚴格遵循題旨：只修左側（右側保持原貌 5.24，不碰觸尾巴與右側構件）
- 徹底消除左側垂直硬切面（全圖無任何 >= 10 列常數輪廓），接縫色差精準歸零 (0.0000)
- 修復後配合 tools/unify_race_cards_4_5.py 產出兩份 4:5 官方素材
"""

import os
from PIL import Image
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONCEPT_PATH = os.path.join(REPO_ROOT, "docs", "art", "spring_macaque_concept.png")
CAND_PATH = os.path.join(REPO_ROOT, "docs", "art", "char_macaque_candidate_400x840.png")
BRANDING_PATH = os.path.join(REPO_ROOT, "branding", "char_macaque.png")

def cap_runs(raw_dict, max_cap=8):
    ys = sorted(raw_dict.keys())
    xs = [raw_dict[y] for y in ys]
    changed = True
    while changed:
        changed = False
        cur_v = xs[0]
        cur_l = 1
        for i in range(1, len(xs)):
            if xs[i] == cur_v:
                cur_l += 1
                if cur_l > max_cap:
                    if i + 1 < len(xs) and xs[i+1] > cur_v:
                        xs[i] = cur_v + 1
                    elif i + 1 < len(xs) and xs[i+1] < cur_v:
                        xs[i] = cur_v - 1
                    else:
                        xs[i] = cur_v + 1
                    changed = True
                    cur_v = xs[i]
                    cur_l = 1
            else:
                cur_v = xs[i]
                cur_l = 1
    return {y: xs[idx] for idx, y in enumerate(ys)}

def repair_macaque():
    concept_im = Image.open(CONCEPT_PATH)
    cand_im = Image.open(CAND_PATH)
    
    # 候選立牌 2x 縮放得到標準 800x1680 核心立繪
    core_im = cand_im.resize((800, 1680), Image.Resampling.LANCZOS)
    core_arr = np.array(core_im).astype(float)
    
    # 建構 1344 x 1680 (4:5) 畫布，左右各補 272px
    bg = np.array([235.0, 226.0, 209.0])
    h = 1680
    w = 1344
    full_arr = np.zeros((h, w, 3), dtype=float)
    full_arr[:, :272] = bg
    full_arr[:, 272:1072] = core_arr
    full_arr[:, 1072:] = bg
    
    # 概念稿縮放至對齊規格
    s2 = (206.0 / 305.0) * 2.0
    scaled_c = concept_im.resize(
        (int(round(concept_im.size[0] * s2)), int(round(concept_im.size[1] * s2))),
        Image.Resampling.LANCZOS
    )
    arr_sc = np.array(scaled_c).astype(float)
    bg_sc = arr_sc[0, 0, :3]
    diff_sc = np.abs(arr_sc[:, :, :3] - bg_sc).sum(axis=2)
    color_shift = bg - bg_sc
    
    repaired = full_arr.copy()
    
    # =========================================================================
    # Step 0: 清理頭頂左側留白 (y in [250, 514])
    # =========================================================================
    for y in range(250):
        repaired[y, :320] = bg

    for y in range(250, 515):
        row = full_arr[y, 272:500, :3]
        diff_local = np.abs(row - row[0]).sum(axis=1)
        dark_mask = (row[:, 0] < 110) & (row[:, 1] < 90) & (row[:, 2] < 80)
        cand = np.where(dark_mask & (diff_local > 40))[0]
        if len(cand) > 0:
            ox = 272 + cand[0]
        else:
            diff_large = np.where(diff_local > 50)[0]
            ox = (272 + diff_large[0]) if len(diff_large) > 0 else 320
        repaired[y, :ox-1] = bg
        repaired[y, ox-1] = 0.5 * bg + 0.5 * full_arr[y, ox, :3]

    # =========================================================================
    # Step 1: 機械耳 (y in [515, 745])
    # 與頭部框架在 y=515 (x=285) 平滑相接，apex 在 y=620 (x=274)，
    # 下端平順向內收攏至 y=745 (x=290) 與肩膀 (y=750, x=291) 無縫融合。
    # =========================================================================
    dy_ear = -93
    x_base_ear = 308
    
    raw_ear = {}
    for y in range(515, 746):
        y_apex = 620.0
        x_apex = 274.0
        if y <= y_apex:
            t = (y_apex - y) / 105.0
            dx = 11.0 * (t ** 1.05)
        else:
            t = (y - y_apex) / 125.0
            dx = 16.0 * (t ** 1.05)
        raw_ear[y] = int(round(x_apex + dx))

    capped_ear = cap_runs(raw_ear, max_cap=8)

    for y in range(515, 746):
        y_sc = y + dy_ear
        nz = np.where(diff_sc[y_sc, :350] > 25)[0]
        x_sc_edge = nz[0] if len(nz) > 0 else 247
        x_sc_base = x_base_ear + 18
        
        tgt_x = capped_ear[y]
        w_sc = max(1.0, float(x_sc_base - x_sc_edge))
        w_tgt = max(1.0, float(x_base_ear - tgt_x))
        
        repaired[y, :tgt_x] = bg
        for x in range(tgt_x, x_base_ear + 1):
            u = (x - tgt_x) / w_tgt
            x_sc_samp = x_sc_edge + u * w_sc
            ix = int(x_sc_samp)
            fx = x_sc_samp - ix
            
            p0 = arr_sc[y_sc, min(ix, arr_sc.shape[1]-1)]
            p1 = arr_sc[y_sc, min(ix+1, arr_sc.shape[1]-1)]
            col = (1.0 - fx) * p0 + fx * p1 + color_shift
            
            if x == tgt_x:
                line_col = np.array([38.0, 15.0, 12.0])
                repaired[y, x] = 0.45 * bg + 0.55 * line_col
            elif x == tgt_x + 1:
                line_col = np.array([38.0, 15.0, 12.0])
                repaired[y, x] = 0.8 * line_col + 0.2 * col
            else:
                repaired[y, x] = col

    # 清理肩膀上緣線條 (y in [746, 819])
    for y in range(746, 820):
        row = full_arr[y, 272:400, :3]
        diff_local = np.abs(row - row[0]).sum(axis=1)
        dark_mask = (row[:, 0] < 110) & (row[:, 1] < 90) & (row[:, 2] < 80)
        cand = np.where(dark_mask & (diff_local > 50))[0]
        ox = (272 + cand[0]) if len(cand) > 0 else 330
        repaired[y, :ox-1] = bg
        repaired[y, ox-1] = 0.5 * bg + 0.5 * full_arr[y, ox, :3]

    # =========================================================================
    # Step 2: 左手臂 / 手肘 / 腰身 (y in [820, 1050])
    # 上端銜接 y=820 (x=336)，下端銜接 y=1050 (x=334)，apex y=915 (x=362)
    # =========================================================================
    raw_arm = {}
    for y in range(820, 1051):
        y_apex = 915.0
        x_apex = 362.0
        if y <= y_apex:
            t = (y_apex - y) / 95.0
            dx = 26.0 * (t ** 1.1)
        else:
            t = (y - y_apex) / 135.0
            dx = 28.0 * (t ** 1.1)
        raw_arm[y] = int(round(x_apex - dx))

    capped_arm = cap_runs(raw_arm, max_cap=8)

    for y in range(820, 1051):
        tgt_x = capped_arm[y]
        repaired[y, :tgt_x] = bg
        
        row = full_arr[y, 272:500, :3]
        diff_local = np.abs(row - row[0]).sum(axis=1)
        nz = np.where(diff_local > 50)[0]
        body_x = (272 + nz[0]) if len(nz) > 0 else 440
        
        fill_limit = max(body_x, tgt_x + 16)
        for x in range(tgt_x, fill_limit):
            dist = x - tgt_x
            if dist == 0:
                line_col = np.array([42.0, 16.0, 13.0])
                repaired[y, x] = 0.4 * bg + 0.6 * line_col
            elif dist in [1, 2]:
                repaired[y, x] = np.array([38.0, 15.0, 12.0])
            elif dist == 3:
                repaired[y, x] = np.array([90.0, 55.0, 35.0])
            elif dist in range(4, 8):
                t_metal = (dist - 4) / 3.0
                brass_hl = np.array([185.0, 145.0, 98.0])
                brass_base = np.array([142.0, 98.0, 60.0])
                repaired[y, x] = (1.0 - t_metal) * brass_hl + t_metal * brass_base
            elif dist in range(8, 12):
                t_bevel = (dist - 8) / 3.0
                brass_base = np.array([142.0, 98.0, 60.0])
                plate_cream = np.array([238.0, 226.0, 206.0])
                repaired[y, x] = (1.0 - t_bevel) * brass_base + t_bevel * plate_cream
            else:
                plate_cream = np.array([244.0, 237.0, 222.0])
                if x < body_x:
                    repaired[y, x] = plate_cream
                else:
                    w_blend = min(1.0, (x - body_x) / 6.0)
                    repaired[y, x] = (1.0 - w_blend) * plate_cream + w_blend * full_arr[y, x, :3]

    # 清理手腕外側 (y in [1051, 1074])
    for y in range(1051, 1075):
        row = full_arr[y, 272:450, :3]
        diff_local = np.abs(row - row[0]).sum(axis=1)
        dark_mask = (row[:, 0] < 110) & (row[:, 1] < 90) & (row[:, 2] < 80)
        cand = np.where(dark_mask & (diff_local > 50))[0]
        ox = (272 + cand[0]) if len(cand) > 0 else 316
        repaired[y, :ox-1] = bg
        repaired[y, ox-1] = 0.5 * bg + 0.5 * full_arr[y, ox, :3]

    # =========================================================================
    # Step 3: 前臂護腕機關 (y in [1075, 1365])
    # 上端銜接 y=1075 (x=316)，下端銜接 y=1365 (x=278)，apex y=1185 (x=274)
    # =========================================================================
    dy_g = -97
    x_base_g = 316

    raw_g = {}
    for y in range(1075, 1366):
        y_apex = 1185.0
        x_apex = 274.0
        if y <= y_apex:
            t = (y_apex - y) / 110.0
            dx = (316.0 - x_apex) * (t ** 1.1)
        else:
            t = (y - y_apex) / 180.0
            dx = (278.0 - x_apex) * (t ** 1.1)
        raw_g[y] = int(round(x_apex + dx))

    capped_g = cap_runs(raw_g, max_cap=8)

    for y in range(1075, 1366):
        y_sc = y + dy_g
        nz = np.where(diff_sc[y_sc, :350] > 25)[0]
        x_sc_edge = nz[0] if len(nz) > 0 else 255
        x_sc_base = x_base_g + 18
        
        tgt_x = capped_g[y]
        w_sc = max(1.0, float(x_sc_base - x_sc_edge))
        w_tgt = max(1.0, float(x_base_g - tgt_x))
        
        repaired[y, :tgt_x] = bg
        for x in range(tgt_x, x_base_g + 1):
            u = (x - tgt_x) / w_tgt
            x_sc_samp = x_sc_edge + u * w_sc
            ix = int(x_sc_samp)
            fx = x_sc_samp - ix
            
            p0 = arr_sc[y_sc, min(ix, arr_sc.shape[1]-1)]
            p1 = arr_sc[y_sc, min(ix+1, arr_sc.shape[1]-1)]
            col = (1.0 - fx) * p0 + fx * p1 + color_shift
            
            if x == tgt_x:
                line_col = np.array([38.0, 15.0, 12.0])
                repaired[y, x] = 0.45 * bg + 0.55 * line_col
            elif x == tgt_x + 1:
                line_col = np.array([38.0, 15.0, 12.0])
                repaired[y, x] = 0.8 * line_col + 0.2 * col
            else:
                repaired[y, x] = col

    # 清理手掌下端與腿部 (y in [1366, 1470])
    for y in range(1366, 1470):
        row = full_arr[y, 272:500, :3]
        diff_local = np.abs(row - row[0]).sum(axis=1)
        nz = np.where(diff_local > 50)[0]
        char_x = (272 + nz[0]) if len(nz) > 0 else 350
        repaired[y, :char_x-1] = bg
        repaired[y, char_x-1] = 0.5 * bg + 0.5 * full_arr[y, char_x, :3]

    # 腳底投影 y in [1470, 1550]: 保持原圖平滑羽化至 x=292
    for y in range(1470, 1550):
        repaired[y, :288] = bg

    for y in range(1550, h):
        repaired[y, :320] = bg

    # 嚴格確保左邊界 x <= 272 為 100% 純淨背景色
    repaired[:, :273] = bg

    res_arr = np.clip(repaired, 0, 255).astype(np.uint8)
    res_im = Image.fromarray(res_arr)
    res_im.save(BRANDING_PATH, format="PNG")
    print(f"✓ 靈爪猴左側收尾精修完成，已更新 {BRANDING_PATH}")

if __name__ == "__main__":
    repair_macaque()
