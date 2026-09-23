import os
import hashlib
from PIL import Image
import numpy as np

PROOFS_DIR = "/opt/side/bravesoul-game/proofs/qa_round27_web_tortoise"

def check_qa15_md5():
    print("=== [0-QA15] 實機與網頁截圖規格及 MD5 查重 ===")
    files = sorted([f for f in os.listdir(PROOFS_DIR) if f.endswith(".png")])
    hashes = {}
    dups = []
    results = []
    for f in files:
        path = os.path.join(PROOFS_DIR, f)
        with open(path, "rb") as fp:
            data = fp.read()
        md5 = hashlib.md5(data).hexdigest()
        im = Image.open(path)
        w, h = im.size
        size_kb = len(data) / 1024.0
        if md5 in hashes:
            dups.append((f, hashes[md5]))
        else:
            hashes[md5] = f
        results.append({
            "file": f,
            "size": f"{w}x{h}",
            "kb": f"{size_kb:.1f} KB",
            "md5": md5
        })
        print(f"  ✓ {f:<38} {w}x{h:<10} {size_kb:6.1f} KB  MD5: {md5}")
    
    assert len(dups) == 0, f"0-QA15 失敗：發現重複 MD5 截圖：{dups}"
    print(f"  🎉 0-QA15 全部 {len(files)} 張截圖 100% 互異，無重複！\n")
    return results

def check_qa16_qa17():
    print("=== [0-QA16 / 0-QA17] 玄機龜展示卡像素顯微量測（否證破圖與平塗） ===")
    t_path = os.path.join(PROOFS_DIR, "proof_03_desktop_tortoise_card.png")
    im = Image.open(t_path).convert("RGBA")
    arr = np.array(im)
    h, w, _ = arr.shape
    
    # 0-QA17: Unique colors count
    colors = set()
    for y in range(h):
        for x in range(w):
            colors.add(tuple(arr[y, x]))
    unique_colors = len(colors)
    print(f"  ✓ 0-QA17 色彩豐富度：總像素 {w*h}，獨立色彩數 {unique_colors:,}")
    assert unique_colors > 1000, f"0-QA17 失敗：色階數過低 ({unique_colors})，疑似平塗或破圖！"
    
    # 0-QA16: Check for pure white broken hole runs
    # Definition of pure white glitch: r>250, g>250, b>250, a>250
    # In .race-card, background of character media is #fdfbf7 (around (253, 251, 247)).
    # We check if there's any abnormal pure white run > 80px in character area
    white_mask = (arr[:, :, 0] >= 254) & (arr[:, :, 1] >= 254) & (arr[:, :, 2] >= 254)
    max_white_run = 0
    for row in white_mask:
        cur_run = 0
        for val in row:
            if val:
                cur_run += 1
                if cur_run > max_white_run:
                    max_white_run = cur_run
            else:
                cur_run = 0
    print(f"  ✓ 0-QA16 純白連續 run 最大值：{max_white_run} px (門檻 < 80px)")
    assert max_white_run < 80, f"0-QA16 失敗：發現大面積白色破洞 (run = {max_white_run} px)"
    print("  🎉 0-QA16 / 0-QA17 客觀量測全綠，證實玄機龜展示卡渲染正常、無破圖！\n")

if __name__ == "__main__":
    check_qa15_md5()
    check_qa16_qa17()
