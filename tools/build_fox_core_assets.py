#!/usr/bin/env python3
"""
tools/build_fox_core_assets.py
Generates the 11 core character assets for Fox (fox mage) in Clockwork Heart:
1. web/media/hero/fox_idle.png (128x128)
2. game/assets/sprites/player/fox_battle.png (128x128)
3. game/assets/sprites/player/fox_walk_{0..3}.png (64x64, 4 frames)
4. game/assets/sprites/player/fox_walk_{0..3}_x3.png (128x128, 4 frames)
5. game/assets/sprites/portraits/fox.png (128x128)
"""

import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"

def main():
    print("=== Building Fox Core Asset Suite ===")
    
    # Source images
    src_idle = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/party/fox_idle.png").convert("RGBA")
    src_portrait = Image.open(f"{REPO_ROOT}/game/assets/sprites/portraits/fox_mage.png").convert("RGBA")
    
    # 1. web/media/hero/fox_idle.png (128x128)
    web_idle_path = f"{REPO_ROOT}/web/media/hero/fox_idle.png"
    src_idle.save(web_idle_path)
    print(f"Saved: {web_idle_path} ({src_idle.size})")
    
    # 2. game/assets/sprites/player/fox_battle.png (128x128)
    battle_path = f"{REPO_ROOT}/game/assets/sprites/player/fox_battle.png"
    src_idle.save(battle_path)
    print(f"Saved: {battle_path} ({src_idle.size})")
    
    # 3. game/assets/sprites/portraits/fox.png (128x128 HUD combat portrait)
    # Scale from 256x256 to 106x106 and center with balanced margins
    portrait_hud = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    p_scaled = src_portrait.resize((106, 106), Image.Resampling.LANCZOS)
    ox = (128 - 106) // 2
    oy = (128 - 106) // 2 + 2
    portrait_hud.paste(p_scaled, (ox, oy), p_scaled)
    portrait_path = f"{REPO_ROOT}/game/assets/sprites/portraits/fox.png"
    portrait_hud.save(portrait_path)
    print(f"Saved: {portrait_path} ({portrait_hud.size}) bbox={portrait_hud.getbbox()}")
    
    # 4. game/assets/sprites/player/fox_walk_{0..3}_x3.png (128x128)
    # and game/assets/sprites/player/fox_walk_{0..3}.png (64x64)
    # Using the standard 4-frame walk displacement cycle matching rabbit and explore_player.gd
    walk_configs = [
        {"dy": 0, "sq_h": 128, "y_off": 0},    # Frame 0: Contact 1 (baseline)
        {"dy": -3, "sq_h": 127, "y_off": -3},  # Frame 1: Peak rise (lifted by 3px)
        {"dy": 1, "sq_h": 127, "y_off": 2},    # Frame 2: Down / Plant (footfall impact)
        {"dy": -2, "sq_h": 128, "y_off": -2},  # Frame 3: Recovery / Intermediate rise
    ]
    
    for i, cfg in enumerate(walk_configs):
        # 128x128 frame
        f_x3 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        if cfg["sq_h"] != 128:
            sq = src_idle.resize((128, cfg["sq_h"]), Image.Resampling.LANCZOS)
            f_x3.paste(sq, (0, cfg["y_off"]), sq)
        else:
            f_x3.paste(src_idle, (0, cfg["y_off"]), src_idle)
            
        path_x3 = f"{REPO_ROOT}/game/assets/sprites/player/fox_walk_{i}_x3.png"
        f_x3.save(path_x3)
        print(f"Saved: {path_x3} ({f_x3.size}) bbox={f_x3.getbbox()}")
        
        # 64x64 frame
        f_64 = f_x3.resize((64, 64), Image.Resampling.LANCZOS)
        path_64 = f"{REPO_ROOT}/game/assets/sprites/player/fox_walk_{i}.png"
        f_64.save(path_64)
        print(f"Saved: {path_64} ({f_64.size}) bbox={f_64.getbbox()}")

    print("=== All 11 files built successfully! ===")

if __name__ == "__main__":
    main()
