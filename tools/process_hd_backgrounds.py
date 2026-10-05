#!/usr/bin/env python3
"""
處理與安裝標準 1080p (1920x1080) 大廳古典機械神殿與戰鬥石徑廢墟底圖資產。
依據 0-ART50 / 0-ART51 規範：
- 禁止拿舊檔就地放大覆寫（open 同路徑又 save 回去）。
- 來源為全新算圖候選資產 (/tmp/*_candidate.png)，經格式轉換與尺寸適配後輸出至 maps/ 目錄。
- 畫風嚴格遵循 Q 版玩具 2D 賽璐珞描邊插畫規範，與角色立繪風格統一。
"""
import os
import sys
from PIL import Image

def main():
    repo_dir = "/opt/side/bravesoul-game/.worktrees/t_805fa24c"
    if not os.path.exists(repo_dir):
        repo_dir = "/opt/side/bravesoul-game"

    maps_dir = os.path.join(repo_dir, "game/assets/sprites/maps")
    os.makedirs(maps_dir, exist_ok=True)

    # 1. 處理大廳全新古典機械神殿底圖 (temple_lobby_bg.png) 到標準 1080p (1920x1080)
    temple_cand = "/tmp/temple_lobby_candidate.png"
    temple_target = os.path.join(maps_dir, "temple_lobby_bg.png")
    if os.path.exists(temple_cand):
        with Image.open(temple_cand) as im:
            im_rgb = im.convert("RGB")
            # 轉換為 1920x1080 標準規格
            im_1080p = im_rgb.resize((1920, 1080), Image.Resampling.LANCZOS)
            im_1080p.save(temple_target, "PNG", optimize=True)
            print(f"Installed temple_lobby_bg.png from {temple_cand} -> {temple_target} ({im_1080p.size})")
    else:
        print(f"Warning: {temple_cand} not found, skipped temple lobby installation.")

    # 2. 處理戰鬥純橫向石徑廢墟底圖 (stone_path_ruins_bg.png) 到標準 1080p (1920x1080)
    battle_cand = "/tmp/battle_ruins_candidate.png"
    stone_target = os.path.join(maps_dir, "stone_path_ruins_bg.png")
    if os.path.exists(battle_cand):
        with Image.open(battle_cand) as im:
            im_rgb = im.convert("RGB")
            im_1080p = im_rgb.resize((1920, 1080), Image.Resampling.LANCZOS)
            im_1080p.save(stone_target, "PNG", optimize=True)
            print(f"Installed stone_path_ruins_bg.png from {battle_cand} -> {stone_target} ({im_1080p.size})")

if __name__ == "__main__":
    main()
