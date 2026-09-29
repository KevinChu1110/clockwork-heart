#!/usr/bin/env python3
import os
import glob

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = glob.glob(f"{REPO_ROOT}/game/assets/sprites/player/poses/lemur/*.import")
files += glob.glob(f"{REPO_ROOT}/game/assets/sprites/player/*lemur_battle*.import")
files += glob.glob(f"{REPO_ROOT}/game/assets/sprites/player/proof_lemur_*.import")

print(f"Removing {len(files)} generated .import files so Godot can generate canonical ctex...")
for f in files:
    try:
        os.remove(f)
        print(f"Removed {os.path.basename(f)}")
    except Exception as e:
        print(f"Error {f}: {e}")
