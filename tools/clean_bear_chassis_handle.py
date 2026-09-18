#!/usr/bin/env python3
"""
tools/clean_bear_chassis_handle.py
精確清除玄軸熊（The Iron Bear）chassis 素體上的舊武器直柄、條紋與懸空鏈條殘留物：
1. 128x128 切片 (paint_bear_amber, paint_iron_quarry, paint_ivory_stock)
2. 512x512 切片 (paint_bear_amber_512, paint_iron_quarry_512, paint_ivory_stock_512)
"""

import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
CHASSIS_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bear/chassis"

# 舊素體殘留切片座標
LEAKED_COORDS_128 = [
    (30, 93), (30, 94), (30, 95), (30, 96), (30, 97), (30, 98),
    (31, 92), (31, 93), (31, 94), (31, 95), (31, 96), (31, 97),
    (32, 92), (32, 93), (32, 94), (32, 95), (32, 96),
    (33, 92), (33, 93), (33, 94), (33, 95), (33, 96),
    (34, 85), (34, 86), (34, 87), (34, 91), (34, 92), (34, 93), (34, 94), (34, 95), (34, 96),
    (35, 85), (35, 86), (35, 87), (35, 88), (35, 91), (35, 92), (35, 93), (35, 94), (35, 95),
    (36, 86), (36, 87), (36, 88), (36, 89), (36, 91), (36, 92), (36, 93), (36, 94), (36, 95),
    (37, 86), (37, 87), (37, 88), (37, 89), (37, 90), (37, 91), (37, 92), (37, 93), (37, 94), (37, 95)
]

VARIANTS = ["paint_bear_amber", "paint_iron_quarry", "paint_ivory_stock"]

def clean_chassis():
    for name in VARIANTS:
        p128 = f"{CHASSIS_DIR}/{name}.png"
        p512 = f"{CHASSIS_DIR}/{name}_512.png"
        
        # 1. 處理 128
        im128 = Image.open(p128).convert("RGBA")
        arr128 = np.array(im128)
        
        # 清除直柄與懸空鏈條
        for x, y in LEAKED_COORDS_128:
            arr128[y, x] = [0, 0, 0, 0]
            
        # 清理握拳手腕處的黃色直柄殘留線（正確座標在 x=86..89, y=82..85）
        fill_color = [35, 42, 56, 255] if "quarry" in name else [50, 55, 68, 255]
        arr128[82, 86] = fill_color
        arr128[83, 87] = fill_color
        arr128[84, 88] = fill_color
        arr128[85, 89] = fill_color
        
        # 清理 x <= 27, y < 110 的邊界雜質
        for y in range(110):
            for x in range(28):
                arr128[y, x] = [0, 0, 0, 0]
                
        clean128 = Image.fromarray(arr128)
        clean128.save(p128)
        print(f"✓ Cleaned 128: {p128}")
        
        # 2. 處理 512
        clean512 = clean128.resize((512, 512), resample=Image.Resampling.LANCZOS)
        arr512 = np.array(clean512)
        
        # 清理在手臂/手肘外側 (x < 114, y < 350) 的微弱垂直線噪點
        for y in range(350):
            for x in range(114):
                arr512[y, x] = [0, 0, 0, 0]
                
        # 清理在左腰外部空間（x in 110..155, y in 335..395）的微弱半透明振鈴噪點
        for y in range(335, 396):
            for x in range(110, 156):
                if arr512[y, x, 3] < 35:
                    arr512[y, x] = [0, 0, 0, 0]
                    
        # 手腕外側左邊界 (x in 110..136, y in 300..350) 任何孤立雜點清空
        for y in range(300, 350):
            for x in range(110, 136):
                if arr512[y, x, 3] < 50:
                    arr512[y, x] = [0, 0, 0, 0]
                    
        # 清理腰部與大腿交界處外側負空間 (x in 150..166, y in 380..412) 的極淡垂直線振鈴殘留 (alpha < 20)
        for y in range(380, 413):
            for x in range(150, 166):
                if arr512[y, x, 3] < 20:
                    arr512[y, x] = [0, 0, 0, 0]
                    
        # 握拳處 512 高清色斑清理：清除殘留之黃色直柄殘留 (R>180, G>150, B<110)
        sub_fist = arr512[326:346, 342:362]
        r_f = sub_fist[:, :, 0].astype(int)
        g_f = sub_fist[:, :, 1].astype(int)
        b_f = sub_fist[:, :, 2].astype(int)
        a_f = sub_fist[:, :, 3].astype(int)
        y_mask = (r_f > 180) & (g_f > 150) & (b_f < 110) & (a_f > 50)
        sub_fist[y_mask] = fill_color
        arr512[326:346, 342:362] = sub_fist
                    
        clean512_final = Image.fromarray(arr512)
        clean512_final.save(p512)
        print(f"✓ Cleaned 512: {p512}")

if __name__ == "__main__":
    clean_chassis()
