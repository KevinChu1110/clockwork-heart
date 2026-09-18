#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"

def clean_weapon():
    p512 = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bear/weapon/wpn_eccentric_gyro_sledge_512.png"
    p128 = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bear/weapon/wpn_eccentric_gyro_sledge.png"
    
    im512 = Image.open(p512).convert("RGBA")
    arr512 = np.array(im512)
    
    # In 512:
    # 1. The dangling chain, yellow ball, and leaked leg are all at y >= 326 for x < 365,
    # and for y >= 333 everywhere (since the hammer head ends at y=332).
    arr512[333:, :] = [0, 0, 0, 0]
    
    # At y in 260..333, remove leaked body armor to the left of the hammer head:
    # The hammer head's left boundary is at x=311.
    for y in range(260, 333):
        for x in range(0, 311):
            arr512[y, x] = [0, 0, 0, 0]
            
    # At y in 325..333, x in 311..332 is the dangling rod connection at the bottom of the grip:
    # Let's clean the dangling rod segment below the grip (y >= 326, x < 336):
    for y in range(326, 333):
        for x in range(311, 336):
            arr512[y, x] = [0, 0, 0, 0]
            
    # Save cleaned 512
    clean512 = Image.fromarray(arr512)
    clean512.save(p512)
    print(f"✓ Cleaned weapon 512: {p512}")
    
    # 128 version:
    # Downsample cleanly with LANCZOS or clean directly
    clean128 = clean512.resize((128, 128), resample=Image.Resampling.LANCZOS)
    clean128.save(p128)
    print(f"✓ Cleaned weapon 128: {p128}")

if __name__ == "__main__":
    clean_weapon()
