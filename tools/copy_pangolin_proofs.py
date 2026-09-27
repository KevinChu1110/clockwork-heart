#!/usr/bin/env python3
import shutil
import os

SRC = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/pangolin"
DST = "/opt/side/bravesoul-game/proofs/t_ea828ac6"
os.makedirs(DST, exist_ok=True)

shutil.copyfile(f"{SRC}/proof_pangolin_all_7_slices.png", f"{DST}/proof_04_pangolin_all_7_slices.png")
shutil.copyfile(f"{SRC}/proof_paperdoll_pangolin_magenta.png", f"{DST}/proof_05_paperdoll_pangolin_magenta.png")
shutil.copyfile(f"{SRC}/proof_paperdoll_pangolin_composite.png", f"{DST}/proof_06_paperdoll_pangolin_composite.png")
print("✓ Proof composites copied to proofs/t_ea828ac6/")
