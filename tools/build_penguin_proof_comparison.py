#!/usr/bin/env python3
"""
tools/build_penguin_proof_comparison.py
Stitches side-by-side proof image for Penguin Real Wardrobe:
1. Bare Chassis (None)
2. Fixed Navigator Greatcoat (costume_navigator_harness)
3. Abyssal Diver Reference (costume_abyssal_diver_cuirass)
"""

import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

PROOFS_DIR = "/opt/side/bravesoul-game/proofs/costume_fix_t_84698e86"
WS_PROOFS_DIR = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_84698e86/proofs"

def build_comparison():
    p_none = f"{PROOFS_DIR}/crop_penguin_none_chassis.png"
    p_fixed = f"{PROOFS_DIR}/crop_penguin_navigator_harness_fixed.png"
    p_ref = f"{PROOFS_DIR}/crop_penguin_abyssal_diver_ref.png"

    img_none = Image.open(p_none).convert("RGBA")
    img_fixed = Image.open(p_fixed).convert("RGBA")
    img_ref = Image.open(p_ref).convert("RGBA")

    w, h = img_none.size
    pad = 20
    header_h = 70
    footer_h = 50
    total_w = w * 3 + pad * 4
    total_h = h + header_h + footer_h

    canvas = Image.new("RGBA", (total_w, total_h), (25, 27, 36, 255))
    draw = ImageDraw.Draw(canvas)

    # Header
    title = "Penguin Real Wardrobe In-Engine: Bare Chassis vs Fixed Navigator Greatcoat vs Abyssal Ref"
    draw.text((pad, 15), title, fill=(255, 208, 40, 255))
    subtitle = "t_84698e86: Outward Triangular Lapels + Flared Hem Skirt + Gold/Ivory Contrasting Trims"
    draw.text((pad, 40), subtitle, fill=(200, 220, 240, 255))

    # Panels
    panels = [
        ("1. [None] 裸機素體 (Bare)", img_none, (180, 190, 205)),
        ("2. [Fixed] 深海導航員大衣 (Masterpiece)", img_fixed, (255, 208, 40)),
        ("3. [Ref] 淵海深潛機關鎧 (Reference)", img_ref, (78, 216, 106))
    ]

    for i, (label, img, col) in enumerate(panels):
        x = pad + i * (w + pad)
        y = header_h

        # panel border box
        draw.rectangle([x - 2, y - 2, x + w + 1, y + h + 1], outline=(60, 70, 95, 255), width=2)
        canvas.paste(img, (x, y))
        draw.text((x + 10, y + h + 12), label, fill=col)

    out_p1 = f"{PROOFS_DIR}/proof_real_wardrobe_penguin_comparison.png"
    out_p2 = f"{WS_PROOFS_DIR}/proof_real_wardrobe_penguin_comparison.png"
    os.makedirs(WS_PROOFS_DIR, exist_ok=True)

    canvas.save(out_p1)
    canvas.save(out_p2)
    print(f"Saved comparison to:\n  {out_p1}\n  {out_p2}")

if __name__ == "__main__":
    build_comparison()
