#!/usr/bin/env python3
import os
from PIL import Image

def main():
    repo_dir = "/opt/side/bravesoul-game"
    
    # 1. 處理 temple_lobby_bg.png 到標準 1080p (1920x1080)
    temple_path = os.path.join(repo_dir, "game/assets/sprites/maps/temple_lobby_bg.png")
    if os.path.exists(temple_path):
        with Image.open(temple_path) as im:
            im_rgb = im.convert("RGB")
            im_1080p = im_rgb.resize((1920, 1080), Image.Resampling.LANCZOS)
            im_1080p.save(temple_path, "PNG", optimize=True)
            print(f"Resized temple_lobby_bg.png to {im_1080p.size}")

    # 2. 處理 stone_path_ruins_bg.png 到標準 1080p (1920x1080)
    candidate_path = "/tmp/battle_ruins_candidate.png"
    stone_path = os.path.join(repo_dir, "game/assets/sprites/maps/stone_path_ruins_bg.png")
    if os.path.exists(candidate_path):
        with Image.open(candidate_path) as im:
            im_rgb = im.convert("RGB")
            im_1080p = im_rgb.resize((1920, 1080), Image.Resampling.LANCZOS)
            im_1080p.save(stone_path, "PNG", optimize=True)
            print(f"Saved stone_path_ruins_bg.png as 1080p ({im_1080p.size})")

            # 額外同步到 battle/ 目錄若有需要
            battle_dir = os.path.join(repo_dir, "game/assets/sprites/battle")
            os.makedirs(battle_dir, exist_ok=True)
            im_1080p.save(os.path.join(battle_dir, "battle_ruins_hd.png"), "PNG", optimize=True)
            im_1080p.save(os.path.join(battle_dir, "battle_ruins_pixel.png"), "PNG", optimize=True)

if __name__ == "__main__":
    main()
