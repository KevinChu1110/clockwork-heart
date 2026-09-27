#!/usr/bin/env python3
from PIL import Image

comp_path = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/otter/proof_paperdoll_otter_composite.png"
im = Image.open(comp_path).convert("RGBA")

base_landmarks = {
    "head_top": (64, 21),
    "ear_l": (38, 38),
    "ear_r": (90, 38),
    "eye_l": (52, 40),
    "eye_r": (76, 40),
    "snout": (64, 49),
    "throat": (64, 58),
    "core": (63, 73),
    "shoulder_l": (46, 68),
    "shoulder_r": (80, 68),
    "arm_l": (36, 78),
    "arm_r": (88, 76),
    "torso": (63, 80),
    "pelvis": (63, 94),
    "hip_l": (46, 96),
    "hip_r": (80, 96),
    "foot_l": (44, 114),
    "foot_r": (82, 114),
    "tail_root": (44, 88),
    "tail_mid": (28, 92),
    "tail_tip": (16, 94),
    "key_mount": (76, 48),
    "key_wing": (88, 32),
}

for name, (x, y) in base_landmarks.items():
    p = im.getpixel((x, y))
    print(f"{name:12s}: ({x:2d}, {y:2d}) -> rgba={p}")
