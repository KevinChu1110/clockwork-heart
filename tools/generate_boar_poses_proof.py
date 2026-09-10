#!/usr/bin/env python3
"""
tools/generate_boar_poses_proof.py
Generates a side-by-side verification sheet for all 6 Boar combat action poses:
  screenshots/proof_boar_combat_poses.png
"""

import os
from typing import cast
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
POSES_DIR = os.path.join(REPO_ROOT, "game/assets/sprites/player/poses/boar")
FONT_PATH = os.path.join(REPO_ROOT, "game/assets/fonts/jf-openhuninn-2.1.ttf")
OUT_PROOF = os.path.join(REPO_ROOT, "screenshots/proof_boar_combat_poses.png")

def get_font(size: int = 14):
    if os.path.exists(FONT_PATH):
        try:
            return ImageFont.truetype(FONT_PATH, size)
        except Exception:
            pass
    return ImageFont.load_default()

def create_proof():
    os.makedirs(os.path.dirname(OUT_PROOF), exist_ok=True)
    poses = ["idle", "telegraph", "attack", "recover", "skill", "hit"]
    titles = [
        "待機 (Idle)",
        "預警蓄力 (Telegraph)",
        "巨錘掄擊 (Attack)",
        "受擊吸震 (Recover)",
        "鍛爐狂暴 (Skill)",
        "受擊後仰 (Hit)",
    ]

    card_w, card_h = 140, 180
    gap = 16
    pad = 20
    total_w = pad * 2 + card_w * 6 + gap * 5
    total_h = pad * 2 + card_h + 40 # title header

    proof = Image.new("RGBA", (total_w, total_h), (255, 253, 248, 255))
    draw = ImageDraw.Draw(proof)

    title_font = get_font(18)
    label_font = get_font(13)
    sub_font = get_font(11)

    # Header title
    draw.text((pad, pad), "《發條之心》鋼牙豕（野豬族）六大戰鬥動作姿態驗證 (128x128 RGBA)", fill=(31, 26, 58, 255), font=title_font)

    top_y = pad + 40
    for idx, (p_name, title) in enumerate(zip(poses, titles)):
        p_path = os.path.join(POSES_DIR, f"{p_name}.png")
        assert os.path.exists(p_path), f"Missing {p_path}"
        im = Image.open(p_path).convert("RGBA")

        x_pos = pad + idx * (card_w + gap)
        y_pos = top_y

        # Card container
        draw.rounded_rectangle([x_pos, y_pos, x_pos + card_w, y_pos + card_h], radius=12, fill=(245, 240, 230, 255), outline=(210, 195, 175, 255), width=1)

        # Paste 128x128 sprite centered in card
        sprite_x = x_pos + (card_w - 128) // 2
        sprite_y = y_pos + 8
        proof.alpha_composite(im, (sprite_x, sprite_y))

        # Text label
        draw.text((x_pos + card_w // 2, y_pos + 142), title, fill=(31, 26, 58, 255), font=label_font, anchor="mm")
        draw.text((x_pos + card_w // 2, y_pos + 162), f"{p_name}.png", fill=(130, 115, 100, 255), font=sub_font, anchor="mm")

    proof.save(OUT_PROOF)
    print(f"✓ Saved proof sheet: {OUT_PROOF} ({total_w}x{total_h})")

if __name__ == "__main__":
    create_proof()
