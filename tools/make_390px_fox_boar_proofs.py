#!/usr/bin/env python3
import os
from PIL import Image

shot_dir = "/opt/side/bravesoul-game/screenshots"

targets = [
    ("proof_battle_fox_full_screen.png", "proof_battle_fox_full_screen_390px.png"),
    ("proof_battle_fox_attack_full_screen.png", "proof_battle_fox_attack_full_screen_390px.png"),
    ("proof_battle_boar_full_screen.png", "proof_battle_boar_full_screen_390px.png"),
    ("proof_battle_boar_attack_full_screen.png", "proof_battle_boar_attack_full_screen_390px.png"),
]

for src_name, out_name in targets:
    src_p = os.path.join(shot_dir, src_name)
    out_p = os.path.join(shot_dir, out_name)
    im = Image.open(src_p)
    w, h = im.size
    new_h = int(h * (390.0 / float(w)))
    im_390 = im.resize((390, new_h), Image.Resampling.LANCZOS)
    im_390.save(out_p)
    print(f"✓ 產生 390px 驗收圖: {out_p} ({im_390.size})")
