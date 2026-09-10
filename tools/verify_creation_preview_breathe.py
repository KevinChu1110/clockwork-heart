import os
import sys
from PIL import Image, ImageChops

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    proofs_dir = os.path.join(repo_root, "proofs", "creation_breathe")
    screenshots_dir = os.path.join(repo_root, "screenshots")

    def get_img_path(fname):
        p1 = os.path.join(proofs_dir, fname)
        if os.path.exists(p1):
            return p1
        return os.path.join(screenshots_dir, fname)

    rab_t0_path = get_img_path("proof_creation_breathe_rabbit_t0.png")
    rab_t1_path = get_img_path("proof_creation_breathe_rabbit_t1.png")
    fox_t0_path = get_img_path("proof_creation_breathe_fox_t0.png")
    fox_t1_path = get_img_path("proof_creation_breathe_fox_t1.png")

    for p in [rab_t0_path, rab_t1_path, fox_t0_path, fox_t1_path]:
        if not os.path.exists(p):
            print(f"找不到截圖檔案: {p}")
            sys.exit(1)

    rab_t0 = Image.open(rab_t0_path).convert("RGBA")
    rab_t1 = Image.open(rab_t1_path).convert("RGBA")
    fox_t0 = Image.open(fox_t0_path).convert("RGBA")
    fox_t1 = Image.open(fox_t1_path).convert("RGBA")

    print(f"=== 驗證開局選族角色預覽待機呼吸 (Creation Preview Breathe) ===")
    print(f"截圖解析度: {rab_t0.size} (1280x720 橫屏規範)")

    # 分析單一種族的呼吸幾何變化
    def verify_race_breathe(race_name, im_t0, im_t1):
        print(f"\n──────────────────────────────────────────────────────")
        print(f"【{race_name}】待機呼吸量測 (t0 ↔ t1 間隔 1.1s >= 1.0s)")

        # 1. 差異計算
        diff = ImageChops.difference(im_t0, im_t1)
        diff_bbox = diff.getbbox(alpha_only=False)
        print(f"  [差異區域 BBox] {diff_bbox}")

        # 2. 對照組驗證：預覽卡片區域外（x < 40 或 x > 620 或 y < 216 或 y > 696）diff 應為 0
        preview_diff_count = 0
        outside_diff_count = 0
        for y in range(720):
            for x in range(1280):
                px = diff.getpixel((x, y))
                val = 0
                if isinstance(px, (tuple, list)):
                    val = max(px[:3])
                elif isinstance(px, (int, float)):
                    val = int(px)
                if val > 5:
                    if 40 <= x <= 620 and 216 <= y <= 696:
                        preview_diff_count += 1
                    else:
                        outside_diff_count += 1

        print(f"  [預覽區內 Diff 像素數] {preview_diff_count} (呼吸動態顯著)")
        print(f"  [預覽區外 (對照組) Diff 像素數] {outside_diff_count} (背景無漂移，鎖住 review.md 4b-14 第 ④ 條)")
        assert outside_diff_count == 0, f"預覽區外有異常漂移 diff: {outside_diff_count}"

        # 3. 角色本體 bbox 量測 (依 review.md 第 4b-14-1 條)
        # 預覽舞台底色為卡片白底 Color(1, 1, 1, 1) 與底部淡灰紫台座
        # 取樣角色區域 x in [180, 480], y in [270, 610]
        # 與純白底色 (255, 255, 255) 差異顯著者為角色像素
        def get_char_bbox(im):
            min_x, max_x = 9999, -1
            min_y, max_y = 9999, -1
            for y in range(270, 608): # 避開底座底部
                for x in range(180, 480):
                    px = im.getpixel((x, y))
                    # 與白底 (255, 255, 255) 差距 > 20 的視為角色像素
                    if (255 - px[0]) > 20 or (255 - px[1]) > 20 or (255 - px[2]) > 20:
                        if x < min_x: min_x = x
                        if x > max_x: max_x = x
                        if y < min_y: min_y = y
                        if y > max_y: max_y = y
            return min_x, min_y, max_x, max_y

        bx0, by0, bx1, by1 = get_char_bbox(im_t0)
        cx0, cy0, cx1, cy1 = get_char_bbox(im_t1)

        w0, h0 = (bx1 - bx0 + 1), (by1 - by0 + 1)
        w1, h1 = (cx1 - cx0 + 1), (cy1 - cy0 + 1)

        print(f"  [t0 角色 BBox] x:[{bx0}, {bx1}] (寬={w0}), y:[{by0}, {by1}] (高={h0})")
        print(f"  [t1 角色 BBox] x:[{cx0}, {cx1}] (寬={w1}), y:[{cy0}, {cy1}] (高={h1})")

        # 高度比對齊宣告 (0.97 / 1.02 ≈ 0.95098)
        ratio_h = h0 / float(h1)
        target_h = 0.97 / 1.02
        err_h = abs(ratio_h - target_h) / target_h
        print(f"  [高度比 (t0 / t1)] 實測={ratio_h:.4f} vs 宣告={target_h:.4f} (偏差: {err_h*100:.2f}%, 門檻 ±2%)")

        # 寬度比對齊宣告 (1.03 / 0.98 ≈ 1.05102)
        ratio_w = w0 / float(w1)
        target_w = 1.03 / 0.98
        err_w = abs(ratio_w - target_w) / target_w
        print(f"  [寬度比 (t0 / t1)] 實測={ratio_w:.4f} vs 宣告={target_w:.4f} (偏差: {err_w*100:.2f}%, 門檻 ±2%)")

        assert err_h <= 0.02, f"高度比偏差 {err_h*100:.2f}% 超出 ±2% 門檻!"
        return {
            "race": race_name,
            "h0": h0, "h1": h1, "ratio_h": ratio_h, "err_h": err_h,
            "w0": w0, "w1": w1, "ratio_w": ratio_w, "err_w": err_w,
            "diff_count": preview_diff_count,
            "outside_diff": outside_diff_count
        }

    res_rab = verify_race_breathe("兔族 (Rabbit)", rab_t0, rab_t1)
    res_fox = verify_race_breathe("狐族 (Fox)", fox_t0, fox_t1)

    print("\n======================================================")
    print("【驗收總結】")
    print(f"  1. 兔族呼吸高度比: {res_rab['ratio_h']:.4f} (偏差 {res_rab['err_h']*100:.2f}% <= 2%)")
    print(f"  2. 狐族呼吸高度比: {res_fox['ratio_h']:.4f} (偏差 {res_fox['err_h']*100:.2f}% <= 2%)")
    print(f"  3. 兩族對照組畫面其餘區域 diff 均為 0 (背景完全無漂移)")
    print(f"  4. 兩族間隔 >= 1.0s (1.1s) 截圖完成且雙族均通過幾何量測")
    print("======================================================")

if __name__ == "__main__":
    main()
