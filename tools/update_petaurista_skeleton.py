#!/usr/bin/env python3
import json
import os

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_gitkeeps(root):
    base_dir = os.path.join(root, "game/assets/sprites/player/paperdoll/petaurista")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(root, "game/assets/sprites/player/poses/petaurista")
    os.makedirs(poses_dir, exist_ok=True)
    poses_keep = os.path.join(poses_dir, ".gitkeep")
    if not os.path.exists(poses_keep):
        with open(poses_keep, "w") as f:
            pass
        print(f"建立 {poses_keep}")

if __name__ == "__main__":
    create_gitkeeps(repo_root)
    print("petaurista 槽位空目錄與 poses 目錄建置完成（僅包含 .gitkeep）")
