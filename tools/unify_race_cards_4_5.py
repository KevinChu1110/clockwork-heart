#!/usr/bin/env python3
"""
統一九族卡片與立牌畫布比例為 4:5 (0.800000)
遵循 references/review.md 0-QA7 規範：
- 將九張來源圖統一步成同一畫布比例 4:5
- 等比置中、左右/上下同底色邊緣留白延伸 (edge-clamp replicate padding)
- 不拉伸變形、不裁切任何武器與發條鑰匙
- 同步產出 branding/char_*.png 與 web/media/hero/char_*.png
"""

import os
import sys
from PIL import Image
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(REPO_ROOT, "branding")
WEB_HERO_DIR = os.path.join(REPO_ROOT, "web", "media", "hero")

RACES = [
    ("rabbit", "白金兔"),
    ("lion", "烈鬃獅"),
    ("fox", "靈尾狐"),
    ("boar", "鋼牙豕"),
    ("macaque", "靈爪猴"),
    ("tiger", "烈焰虎"),
    ("crane", "雲嵐鶴"),
    ("bear", "玄軸熊"),
    ("penguin", "蒸氣企鵝"),
    ("tortoise", "玄機龜"),
    ("elephant", "鋼岳象"),
]

def pad_to_4_5(im: Image.Image, race_name: str) -> Image.Image:
    w, h = im.size
    arr = np.array(im)
    
    if (w == 800 and h == 1680) or (w == 1344 and h == 1680):
        # Target: 1344 x 1680 (1344 / 1680 = 0.8 exact)
        if w == 1344:
            # 若已經是補過邊的 1344x1680，取出核心 800x1680 重做乾淨補邊
            arr = arr[:, 272:1072, :]
            w, h = 800, 1680
        target_w, target_h = 1344, 1680
        pad_l = 272
        pad_r = 272
        # 改採背景米色填滿（取邊角乾淨背景色，避免將邊緣角色像素水平延展產生 smear 條紋）
        bg_l = arr[0, 0, :]
        bg_r = arr[0, -1, :]
        l_pad = np.full((h, pad_l, arr.shape[2]), bg_l, dtype=arr.dtype)
        r_pad = np.full((h, pad_r, arr.shape[2]), bg_r, dtype=arr.dtype)
        res_arr = np.concatenate([l_pad, arr, r_pad], axis=1)
        res = Image.fromarray(res_arr)
    elif w == 928 and h == 1152:
        # Target: 928 x 1160 (928 / 1160 = 0.8 exact)
        target_w, target_h = 928, 1160
        pad_t = 4
        pad_b = 4
        t_pad = np.repeat(arr[0:1, :, :], pad_t, axis=0)
        b_pad = np.repeat(arr[-1:, :, :], pad_b, axis=0)
        res_arr = np.concatenate([t_pad, arr, b_pad], axis=0)
        res = Image.fromarray(res_arr)
    elif w == 860 and h == 1152:
        # Target: 928 x 1160 (928 / 1160 = 0.8 exact)
        target_w, target_h = 928, 1160
        pad_l = 34
        pad_r = 34
        pad_t = 4
        pad_b = 4
        l_pad = np.repeat(arr[:, 0:1, :], pad_l, axis=1)
        r_pad = np.repeat(arr[:, -1:, :], pad_r, axis=1)
        temp = np.concatenate([l_pad, arr, r_pad], axis=1)
        t_pad = np.repeat(temp[0:1, :, :], pad_t, axis=0)
        b_pad = np.repeat(temp[-1:, :, :], pad_b, axis=0)
        res_arr = np.concatenate([t_pad, temp, b_pad], axis=0)
        res = Image.fromarray(res_arr)
    else:
        # Generic 4:5 pad
        target_w = int(round(h * 0.8)) if w / h < 0.8 else w
        target_h = h if w / h < 0.8 else int(round(w / 0.8))
        pad_w = target_w - w
        pad_h = target_h - h
        pad_l = pad_w // 2
        pad_r = pad_w - pad_l
        pad_t = pad_h // 2
        pad_b = pad_h - pad_t
        l_pad = np.repeat(arr[:, 0:1, :], pad_l, axis=1) if pad_l > 0 else np.zeros((h, 0, arr.shape[2]), dtype=arr.dtype)
        r_pad = np.repeat(arr[:, -1:, :], pad_r, axis=1) if pad_r > 0 else np.zeros((h, 0, arr.shape[2]), dtype=arr.dtype)
        temp = np.concatenate([l_pad, arr, r_pad], axis=1)
        t_pad = np.repeat(temp[0:1, :, :], pad_t, axis=0) if pad_t > 0 else np.zeros((0, temp.shape[1], arr.shape[2]), dtype=arr.dtype)
        b_pad = np.repeat(temp[-1:, :, :], pad_b, axis=0) if pad_b > 0 else np.zeros((0, temp.shape[1], arr.shape[2]), dtype=arr.dtype)
        res_arr = np.concatenate([t_pad, temp, b_pad], axis=0)
        res = Image.fromarray(res_arr)
        
    assert abs(res.size[0] / res.size[1] - 0.8) < 1e-6, f"{race_name} ratio mismatch: {res.size}"
    return res

def main():
    print("=== 統一九族卡片畫布比例為 4:5 ===")
    
    for race_id, race_label in RACES:
        src_path = os.path.join(BRANDING_DIR, f"char_{race_id}.png")
        assert os.path.exists(src_path), f"Missing {src_path}"
        
        im = Image.open(src_path)
        orig_size = im.size
        orig_ratio = orig_size[0] / orig_size[1]
        
        res = pad_to_4_5(im, race_label)
        new_size = res.size
        new_ratio = new_size[0] / new_size[1]
        
        # Save to branding/
        dst_branding = os.path.join(BRANDING_DIR, f"char_{race_id}.png")
        res.save(dst_branding, format="PNG")
        
        # Save to web/media/hero/
        dst_web = os.path.join(WEB_HERO_DIR, f"char_{race_id}.png")
        res.save(dst_web, format="PNG")
        
        print(f"  ✓ [{race_label:4s} ({race_id:8s})]: {orig_size[0]}x{orig_size[1]} ({orig_ratio:.4f}) -> {new_size[0]}x{new_size[1]} ({new_ratio:.6f})")
    
    print("\n✓ 九族卡片素材已全部統一為 4:5 比例並寫入 branding/ 與 web/media/hero/！")

if __name__ == "__main__":
    main()
