#!/usr/bin/env python3
import shutil

src_base = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/cat"
dst_base = "/opt/side/bravesoul-game/proofs/t_5ff42afe"

shutil.copyfile(f"{src_base}/proof_cat_all_7_slices.png", f"{dst_base}/proof_04_cat_all_7_slices.png")
shutil.copyfile(f"{src_base}/proof_paperdoll_cat_magenta.png", f"{dst_base}/proof_05_paperdoll_cat_magenta.png")
shutil.copyfile(f"{src_base}/proof_paperdoll_cat_composite.png", f"{dst_base}/proof_06_paperdoll_cat_composite.png")
print("✓ Copied proof composites to proofs/t_5ff42afe/")
