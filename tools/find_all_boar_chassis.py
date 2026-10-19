#!/usr/bin/env python3
import os

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

candidates = []
for root, dirs, files in os.walk(REPO_ROOT):
    for f in files:
        if ("boar" in f.lower() or "chassis" in f.lower()) and f.endswith(".png"):
            candidates.append(os.path.join(root, f))

for c in sorted(candidates):
    if "paperdoll" in c or "hero" in c or "proof" in c:
        print(c)
