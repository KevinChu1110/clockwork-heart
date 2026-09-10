#!/usr/bin/env python3
import os
import sys
from PIL import Image, ImageChops

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    shot_dir = os.path.join(base_dir, "screenshots")
    proof_dir = os.path.join(base_dir, "proofs", "battle_breathe")
    os.makedirs(proof_dir, exist_ok=True)

    p0 = os.path.join(shot_dir, "proof_battle_idle_breathe_t0.png")
    p1 = os.path.join(shot_dir, "proof_battle_idle_breathe_t1.png")
    patk = os.path.join(shot_dir, "proof_battle_attack_strike.png")
    pa = os.path.join(shot_dir, "proof_battle_equipped_costume_a.png")
    pb = os.path.join(shot_dir, "proof_battle_equipped_costume_b.png")

    for p in [p0, p1, patk, pa, pb]:
        assert os.path.exists(p), f"缺少檔案: {p}"

    img0 = Image.open(p0).convert("RGBA")
    img1 = Image.open(p1).convert("RGBA")
    img_atk = Image.open(patk).convert("RGBA")
    imga = Image.open(pa).convert("RGBA")
    imgb = Image.open(pb).convert("RGBA")

    print(f"t0 截圖尺寸: {img0.size}")
    print(f"t1 截圖尺寸: {img1.size}")
    print(f"attack 截圖尺寸: {img_atk.size}")
    print(f"costume_a 尺寸: {imga.size}")
    print(f"costume_b 尺寸: {imgb.size}")

    for name, im in [("t0", img0), ("t1", img1), ("attack", img_atk), ("costume_a", imga), ("costume_b", imgb)]:
        assert im.size == (1280, 720), f"{name} 尺寸不為 1280x720"

    # 1. 驗證戰鬥待機呼吸 (t0 vs t1, 間隔 >= 1.0s)
    diff_t = ImageChops.difference(img0, img1)
    bbox_t = diff_t.getbbox(alpha_only=False)
    assert bbox_t is not None, "t0 與 t1 截圖完全相同，未發生呼吸縮放！"
    print(f"✓ 戰鬥待機呼吸差分 bbox (t0 vs t1): {bbox_t}")

    b_t = diff_t.tobytes()
    diff_pixels_t = sum(1 for i in range(0, len(b_t), 4) if b_t[i] > 0 or b_t[i+1] > 0 or b_t[i+2] > 0)
    print(f"✓ 戰鬥待機呼吸差異像素數 (t0 vs t1): {diff_pixels_t}")
    assert diff_pixels_t > 500, f"呼吸縮放差異像素數過低 ({diff_pixels_t})"

    # 驗證背景/敵方區域差異接近 0 (鎖住 review.md 4b-14 第 ④ 條：背景沒漂移)
    # 敵方區域在畫面右側 x > 700
    enemy_crop_diff = diff_t.crop((700, 150, 1200, 550))
    b_e = enemy_crop_diff.tobytes()
    enemy_diff_pixels = sum(1 for i in range(0, len(b_e), 4) if b_e[i] > 8 or b_e[i+1] > 8 or b_e[i+2] > 8)
    print(f"✓ 敵方區域差異像素數 (應接近 0): {enemy_diff_pixels}")
    assert enemy_diff_pixels < 50, f"非玩家區域發生非預期漂移: {enemy_diff_pixels}"

    # 2. 驗證出手攻擊姿態相異 (proof_battle_attack_strike.png vs idle)
    diff_atk = ImageChops.difference(img0, img_atk)
    bbox_atk = diff_atk.getbbox(alpha_only=False)
    assert bbox_atk is not None, "攻擊畫面與待機畫面完全相同！"
    b_atk = diff_atk.tobytes()
    diff_pixels_atk = sum(1 for i in range(0, len(b_atk), 4) if b_atk[i] > 0 or b_atk[i+1] > 0 or b_atk[i+2] > 0)
    print(f"✓ 出手攻擊 vs 待機差分 bbox: {bbox_atk}")
    print(f"✓ 出手攻擊差異像素數: {diff_pixels_atk}")
    assert diff_pixels_atk > 1000, f"出手攻擊差異像素數過低 ({diff_pixels_atk})"

    # 3. 驗證換裝 (costume_a vs costume_b)
    diff_ab = ImageChops.difference(imga, imgb)
    bbox_ab = diff_ab.getbbox(alpha_only=False)
    assert bbox_ab is not None, "外裝 A 與外裝 B 完全相同！"
    b_ab = diff_ab.tobytes()
    diff_pixels_ab = sum(1 for i in range(0, len(b_ab), 4) if b_ab[i] > 0 or b_ab[i+1] > 0 or b_ab[i+2] > 0)
    print(f"✓ 換裝差分 bbox (costume_a vs costume_b): {bbox_ab}")
    print(f"✓ 換裝差異像素數: {diff_pixels_ab} (標準 > 10000)")
    assert diff_pixels_ab > 10000, f"換裝差異像素數未達標 ({diff_pixels_ab} <= 10000)"

    # 4. 產出特寫對照圖供視覺審查
    # 角色區域大約在 x: 180~460, y: 180~500
    char_box = (
        max(0, bbox_t[0] - 20),
        max(0, bbox_t[1] - 20),
        min(img0.width, bbox_t[2] + 20),
        min(img0.height, bbox_t[3] + 20)
    )
    print(f"✓ 角色呼吸特寫範圍: {char_box}")

    crop0 = img0.crop(char_box)
    crop1 = img1.crop(char_box)
    crop_atk = img_atk.crop(char_box)

    w, h = crop0.size
    compare_breathe = Image.new("RGBA", (w * 2 + 10, h), (30, 30, 30, 255))
    compare_breathe.paste(crop0, (0, 0))
    compare_breathe.paste(crop1, (w + 10, 0))
    compare_breathe_path = os.path.join(proof_dir, "proof_battle_breathe_compare.png")
    compare_breathe.save(compare_breathe_path)
    compare_breathe.save(os.path.join(shot_dir, "proof_battle_breathe_compare.png"))
    print(f"✓ 儲存呼吸兩刻對照圖: {compare_breathe_path}")

    # 3-Box 彙整圖 (Idle t0 | Idle t1 | Attack)
    box3 = Image.new("RGBA", (w * 3 + 20, h), (25, 25, 30, 255))
    box3.paste(crop0, (0, 0))
    box3.paste(crop1, (w + 10, 0))
    box3.paste(crop_atk, (w * 2 + 20, 0))
    box3_path = os.path.join(proof_dir, "proof_battle_breathe_3box.png")
    box3.save(box3_path)
    box3.save(os.path.join(shot_dir, "proof_battle_breathe_3box.png"))
    print(f"✓ 儲存 3-Box 特寫彙整圖: {box3_path}")

    # 換裝對照圖
    crop_ca = imga.crop(char_box)
    crop_cb = imgb.crop(char_box)
    compare_costume = Image.new("RGBA", (w * 2 + 10, h), (30, 30, 30, 255))
    compare_costume.paste(crop_ca, (0, 0))
    compare_costume.paste(crop_cb, (w + 10, 0))
    costume_path = os.path.join(proof_dir, "proof_battle_costume_compare.png")
    compare_costume.save(costume_path)
    compare_costume.save(os.path.join(shot_dir, "proof_battle_costume_compare.png"))
    print(f"✓ 儲存雙外裝待機對照圖: {costume_path}")

    print("\n所有客觀量測檢驗全部通過！")

if __name__ == "__main__":
    main()
