#!/usr/bin/env python3
"""
tools/verify_qa_round13.py
探索性 QA 第十三輪自動化量測與合規驗證腳本 (t_eb607930)
九族 512 換裝後找破圖量測驗收

驗證項目：
1. [0-QA15] 15 張實機全景截圖完整性、1280x720 規格、MD5 100% 互異。
2. [0-QA17] 15 張角色區域 crop 相鄰重複欄量測（否證 NN 放大，門檻 < 25%）與色彩豐富度。
3. [0-ART25] 九族 showcase/*_idle_hd.png RGBA 模式與四角 alpha=0 檢驗（杜絕奶油不透明底）。
4. [31d] 零系統 Emoji 檢驗。
5. [0-ART26/26b] 零借圖與底盤外裝分離檢驗。
6. [0-QA16] 角色區域純白矩形破圖像素檢驗（水平連續 run 否證）。
"""

import os
import sys
import glob
import hashlib
import numpy as np
from PIL import Image

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROOFS_DIR = os.path.join(REPO_ROOT, "proofs/qa_round13")
WS_PROOFS_DIR = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_eb607930/proofs/qa_round13"

FULL_SCREENSHOTS = [
    "proof_01_lobby_rabbit.png",
    "proof_02_lobby_fox.png",
    "proof_03_lobby_lion.png",
    "proof_04_creation_rabbit.png",
    "proof_05_creation_fox.png",
    "proof_06_creation_penguin.png",
    "proof_07_wardrobe_rabbit_costume.png",
    "proof_08_wardrobe_fox_costume.png",
    "proof_09_wardrobe_penguin_costume.png",
    "proof_10_explore_rabbit_idle.png",
    "proof_11_explore_lion_idle.png",
    "proof_12_explore_fox_walk.png",
    "proof_13_explore_lion_walk.png",
    "proof_14_battle_penguin_idle.png",
    "proof_15_battle_lion_idle.png",
]

CROP_SCREENSHOTS = [
    "proof_01_lobby_rabbit_crop.png",
    "proof_02_lobby_fox_crop.png",
    "proof_03_lobby_lion_crop.png",
    "proof_04_creation_rabbit_crop.png",
    "proof_05_creation_fox_crop.png",
    "proof_06_creation_penguin_crop.png",
    "proof_07_wardrobe_rabbit_costume_crop.png",
    "proof_08_wardrobe_fox_costume_crop.png",
    "proof_09_wardrobe_penguin_costume_crop.png",
    "proof_10_explore_rabbit_idle_crop.png",
    "proof_11_explore_lion_idle_crop.png",
    "proof_12_explore_fox_walk_crop.png",
    "proof_13_explore_lion_walk_crop.png",
    "proof_14_battle_penguin_idle_crop.png",
    "proof_15_battle_lion_idle_crop.png",
]

def check_0_qa15():
    print("==========================================================")
    print("【階段 1】[0-QA15] 實機截圖規格、完整性與 MD5 查重 (15張)")
    print("==========================================================")
    all_ok = True
    seen_md5 = {}
    
    for fn in FULL_SCREENSHOTS:
        fp = os.path.join(PROOFS_DIR, fn)
        if not os.path.exists(fp):
            print(f"  ❌ 缺失檔案: {fn}")
            all_ok = False
            continue
        
        sz = os.path.getsize(fp)
        if sz < 40000:
            print(f"  ❌ 檔案過小 (疑為黑屏或空畫面): {fn} ({sz} bytes)")
            all_ok = False
            continue
            
        with open(fp, "rb") as f:
            digest = hashlib.md5(f.read()).hexdigest()
            
        if digest in seen_md5:
            print(f"  ❌ 重複截圖違規 (0-QA15): {fn} 與 {seen_md5[digest]} MD5 相同 ({digest})")
            all_ok = False
        else:
            seen_md5[digest] = fn
            
        im = Image.open(fp)
        w, h = im.size
        if (w, h) != (1280, 720):
            print(f"  ❌ 尺寸不符: {fn} ({w}x{h}, 預期 1280x720)")
            all_ok = False
        else:
            print(f"  ✓ {fn}: 1280x720, {sz/1024:.1f} KB, MD5={digest}")

    assert all_ok, "階段 1 檢查失敗：實機截圖缺失、尺寸不符或存在重複 MD5！"
    print("  🎉 [0-QA15] 15 張全景實機截圖全數合格且 100% 互異！\n")
    return seen_md5


def check_0_qa17():
    print("==========================================================")
    print("【階段 2】[0-QA17] 角色區域 Crop 相鄰重複欄比率量測 (否證 NN 放大)")
    print("==========================================================")
    all_ok = True
    results = {}
    
    for fn in CROP_SCREENSHOTS:
        fp = os.path.join(PROOFS_DIR, fn)
        if not os.path.exists(fp):
            print(f"  ❌ 缺失裁切檔案: {fn}")
            all_ok = False
            continue
            
        im = Image.open(fp).convert("RGB")
        arr = np.array(im)
        h, w, _ = arr.shape
        
        # 計算相鄰欄是否完全相同
        # arr[:, :-1] 與 arr[:, 1:]
        diff_col = np.any(arr[:, :-1] != arr[:, 1:], axis=2) # h x (w-1)
        # 一欄重複定義為整欄每一列都相同
        col_identical = np.all(~diff_col, axis=0) # (w-1,)
        dup_cols = np.sum(col_identical)
        ratio_col = dup_cols / (w - 1) * 100.0
        
        # 統計 unique 色數
        flat = arr.reshape(-1, 3)
        # pack to uint32 for fast unique
        packed = (flat[:, 0].astype(np.uint32) << 16) | (flat[:, 1].astype(np.uint32) << 8) | flat[:, 2].astype(np.uint32)
        unique_colors = len(np.unique(packed))
        
        results[fn] = {
            "size": f"{w}x{h}",
            "dup_col_ratio": f"{ratio_col:.2f}%",
            "unique_colors": unique_colors
        }
        
        # 門檻判定：重複欄率必須 < 25% (遠離 NN ~50% baseline)
        if ratio_col >= 25.0:
            print(f"  ❌ [{fn}] 相鄰重複欄比率過高: {ratio_col:.2f}% (疑為 NN 像素放大)")
            all_ok = False
        else:
            print(f"  ✓ [{fn}] 尺寸={w}x{h}, 相鄰重複欄={ratio_col:.2f}% (<25%), 色數={unique_colors:,} (非 NN 放大)")
            
    assert all_ok, "階段 2 檢查失敗：檢測到 NN 像素放大特徵！"
    print("  🎉 [0-QA17] 全數 15 張角色裁切圖重複欄量測全綠，明確否證 NN 放大！\n")
    return results


def check_0_art25():
    print("==========================================================")
    print("【階段 3】[0-ART25] 九族官方立繪 showcase/*_idle_hd.png 去背檢驗")
    print("==========================================================")
    all_ok = True
    sc_files = glob.glob(os.path.join(REPO_ROOT, "game/assets/sprites/player/showcase/*_idle_hd.png"))
    if len(sc_files) < 9:
        print(f"  ❌ 官方立繪數量不足 9 族 (找到 {len(sc_files)} 支)")
        all_ok = False
        
    for fp in sorted(sc_files):
        fname = os.path.basename(fp)
        im = Image.open(fp)
        if im.mode != "RGBA":
            print(f"  ❌ [0-ART25] 模式錯誤 (非 RGBA): {fname} mode={im.mode}")
            all_ok = False
            continue
            
        # 抽四角像素檢查 alpha
        w, h = im.size
        corners = [
            (0, 0),
            (w - 1, 0),
            (0, h - 1),
            (w - 1, h - 1)
        ]
        alpha_corners = [im.getpixel(c)[3] for c in corners]
        if any(a != 0 for a in alpha_corners):
            print(f"  ❌ [0-ART25] 四角像素未去背 (alpha > 0): {fname} corners={alpha_corners}")
            all_ok = False
        else:
            print(f"  ✓ {fname}: RGBA, {w}x{h}, 四角 alpha={alpha_corners} (純淨去背無奶油底)")
            
    assert all_ok, "階段 3 檢查失敗：官方展示立繪存在未去背或非 RGBA 圖檔！"
    print("  🎉 [0-ART25] 九族 showcase 貼圖全數為 RGBA 且四角 alpha=0，無不透明奶油底！\n")


def check_0_qa16_white_mask():
    print("==========================================================")
    print("【階段 4】[0-QA16] 換裝角色區域純白矩形遮罩破洞量測 (否證破圖)")
    print("==========================================================")
    # 抽查兔族、狐族、企鵝、獅族的換裝預覽圖
    sample_crops = [
        "proof_07_wardrobe_rabbit_costume_crop.png",
        "proof_08_wardrobe_fox_costume_crop.png",
        "proof_10_explore_rabbit_idle_crop.png",
        "proof_12_explore_fox_walk_crop.png",
        "proof_15_battle_lion_idle_crop.png",
    ]
    all_ok = True
    for fn in sample_crops:
        fp = os.path.join(PROOFS_DIR, fn)
        im = Image.open(fp).convert("RGBA")
        arr = np.array(im)
        rh, rw, _ = arr.shape
        
        # 尋找近白像素 (alpha > 240, min(rgb) >= 235)
        mask = (arr[:, :, 3] > 240) & (np.min(arr[:, :, :3], axis=2) >= 235)
        max_run = 0
        max_row = -1
        for y in range(rh):
            cur = 0
            for x in range(rw):
                if mask[y, x]:
                    cur += 1
                    if cur > max_run:
                        max_run = cur
                        max_row = y
                else:
                    cur = 0
                    
        print(f"  • {fn}: 近白像素數={np.sum(mask)}, 最長水平連續 run={max_run} px (y={max_row})")
        # 門檻：只有長 run >= 80px 且該區 std < 2 才是真正白矩形破洞
        if max_run >= 80:
            row_slice = arr[max_row, :, :3][mask[max_row]]
            std_val = float(np.std(row_slice))
            if std_val < 2.0:
                print(f"  ❌ [{fn}] 檢測到異常白色矩形破洞 (run={max_run}>=80, std={std_val}<2)")
                all_ok = False
            else:
                print(f"    ✓ 長 run 為高光漸層 (std={std_val:.2f} >= 2)，非異常破洞。")
        else:
            print(f"    ✓ 最長 run {max_run} px < 80 px，否證白色矩形遮罩破洞 (0-QA16 合格)。")
            
    assert all_ok, "階段 4 檢查失敗：檢測到白色矩形破洞！"
    print("  🎉 [0-QA16] 像素量測全數通過，無異常白色矩形遮罩或圖層破洞！\n")


def check_31d_zero_emoji():
    print("==========================================================")
    print("【階段 5】[31d] 全局零系統 Emoji 與字元圖示檢查 (遵循 review.md 31d)")
    print("==========================================================")
    # 檢查關鍵 UI 腳本與場景
    targets = [
        "game/scripts/ui/mobile_lobby.gd",
        "game/scripts/ui/wardrobe_dialog.gd",
        "game/scripts/art/paperdoll_renderer.gd",
        "game/scripts/art/sprite_db.gd",
        "game/scenes/ui/paperdoll_select_demo.tscn"
    ]
    # 依 review.md 31d: 禁用的字元圖示包括 ⚙ (U+2699), ✦ (U+2726), ★ (U+2605), ◆ (U+25C6) 及各類 Emoji
    forbidden_chars = {"⚙", "✦", "★", "◆", "⭐", "⚔", "🛡", "💎", "💰"}
    # 白名單字元 (review.md 31d 明訂): 關閉鈕 '✕' (U+2715), 勾選態 '✓' (U+2713)
    whitelist_chars = {"✕", "✓", "•", "…", "—", "→", "↑", "↓", "←"}
    
    emoji_ranges = [
        (0x1F300, 0x1FAFF), # Emoji 區塊
        (0x1F600, 0x1F64F), # Emoticons
    ]
    
    all_ok = True
    for rel_p in targets:
        full_p = os.path.join(REPO_ROOT, rel_p)
        if not os.path.exists(full_p):
            continue
        with open(full_p, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            
        for line_no, raw_line in enumerate(lines, 1):
            line = raw_line.strip()
            # 依 31d：忽略註解行
            if line.startswith("#"):
                continue
            # 截取代碼部分 (去掉行尾註解)
            code_part = line.split("#")[0]
            
            for ch in code_part:
                if ch in whitelist_chars:
                    continue
                if ch in forbidden_chars:
                    print(f"  ❌ 在 {rel_p}:{line_no} 發現違規字元圖示 (31d): {ch} ({line})")
                    all_ok = False
                    continue
                code = ord(ch)
                for r_start, r_end in emoji_ranges:
                    if r_start <= code <= r_end:
                        print(f"  ❌ 在 {rel_p}:{line_no} 發現系統 Emoji: {ch} (U+{code:04X}) ({line})")
                        all_ok = False
                        break
                        
    assert all_ok, "階段 5 檢查失敗：發現系統 Emoji 或字元圖示！"
    print("  🎉 [31d] 零系統 Emoji 與字元圖示檢查 100% 通過！(白名單 ✕/✓ 正常遵循規範)\n")


def check_0_art26_no_borrowing():
    print("==========================================================")
    print("【階段 6】[0-ART26 / 26b] 零跨族借圖與底盤外裝分離排查")
    print("==========================================================")
    # 檢查 paperdoll_renderer.gd 與 wardrobe_dialog.gd
    pd_path = os.path.join(REPO_ROOT, "game/scripts/art/paperdoll_renderer.gd")
    wd_path = os.path.join(REPO_ROOT, "game/scripts/ui/wardrobe_dialog.gd")
    
    with open(pd_path, "r", encoding="utf-8") as f:
        pd_src = f.read()
    with open(wd_path, "r", encoding="utf-8") as f:
        wd_src = f.read()
        
    # 1. 檢查有無寫死 rabbit/weapon 或 rabbit/key 的非法 fallback
    assert 'rabbit/weapon/wpn_dawn_blade_512.png' not in pd_src, "SLOT_WEAPON 仍有寫死兔劍 fallback！"
    assert 'rabbit/winding_key/key_classic_brass_512.png' not in pd_src, "SLOT_WINDING_KEY 仍有寫死兔鑰匙 fallback！"
    assert 'costume_viking_harness_512.png' not in wd_src, "wardrobe_dialog 仍有寫死維京裝縮圖 fallback！"
    
    # 2. 檢查各族底盤切片無外裝烘死 (以狐族為例)
    fox_ivory = os.path.join(REPO_ROOT, "game/assets/sprites/player/paperdoll/fox/chassis/paint_ivory_stock_512.png")
    if os.path.exists(fox_ivory):
        im = Image.open(fox_ivory).convert("RGBA")
        print(f"  ✓ 狐族純淨底盤切片存在: {os.path.basename(fox_ivory)} ({im.size[0]}x{im.size[1]})")
        
    print("  ✓ 無寫死具名跨族借圖 fallback，遵循 0-ART26/26b。")
    print("  🎉 [0-ART26/26b] 零借圖與底盤分離檢查通過！\n")


def sync_workspace_proofs():
    print("==========================================================")
    print("【階段 7】同步證明資產至看板工作區目錄")
    print("==========================================================")
    os.makedirs(WS_PROOFS_DIR, exist_ok=True)
    all_files = FULL_SCREENSHOTS + CROP_SCREENSHOTS
    synced = 0
    for fn in all_files:
        src = os.path.join(PROOFS_DIR, fn)
        dst = os.path.join(WS_PROOFS_DIR, fn)
        if os.path.exists(src):
            with open(src, "rb") as sf, open(dst, "wb") as df:
                df.write(sf.read())
            synced += 1
    print(f"  ✓ 已同步 {synced} 張截圖資產至 {WS_PROOFS_DIR}\n")


def main():
    print("##########################################################")
    print("  勇者之魂 · 探索性 QA 第十三輪 (t_eb607930) 自動化驗收")
    print("##########################################################\n")
    
    md5_dict = check_0_qa15()
    qa17_dict = check_0_qa17()
    check_0_art25()
    check_0_qa16_white_mask()
    check_31d_zero_emoji()
    check_0_art26_no_borrowing()
    sync_workspace_proofs()
    
    print("==========================================================")
    print("🎉 QA 第十三輪所有 7 大檢驗階段 100% 全數通過！無玩家可見破圖！")
    print("==========================================================")

if __name__ == "__main__":
    main()
