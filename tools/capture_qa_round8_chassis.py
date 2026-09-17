#!/usr/bin/env python3
"""
tools/capture_qa_round8_chassis.py
Generates zoomed high-resolution chassis comparison and audit cards for:
- Bear (3 paints)
- Penguin (3 paints)
- Tiger (3 paints)
- Crane (3 paints)
Saves to /opt/side/bravesoul-game/proofs/qa_round8/ and workspace.
"""

import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
OUT_DIRS = [
    f"{REPO_ROOT}/proofs/qa_round8",
    "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_c46b102c/proofs/qa_round8"
]

RACES_CHASSIS = {
    "bear": {
        "title": "玄軸熊 (Bear) Chassis 三款塗裝對照驗收",
        "out_name": "proof_13_chassis_bear_comparison.png",
        "paints": [
            ("paint_ivory_stock.png", "原廠象牙白 (Ivory Stock)"),
            ("paint_iron_quarry.png", "重裝礦山玄鐵灰 (Iron Quarry)"),
            ("paint_bear_amber.png", "琥珀暖黃原漆 (Bear Amber)")
        ]
    },
    "penguin": {
        "title": "蒸氣企鵝 (Penguin) Chassis 三款塗裝對照驗收 (0-ART19/20/0-QA8)",
        "out_name": "proof_14_chassis_penguin_comparison.png",
        "paints": [
            ("paint_ivory_stock.png", "原廠象牙白 (Ivory Stock)"),
            ("paint_penguin_navy.png", "蒸氣海軍深藍 (Penguin Navy)"),
            ("paint_polar_frost.png", "極光冰川銀白 (Polar Frost)")
        ]
    },
    "tiger": {
        "title": "烈焰虎 (Tiger) Chassis 三款塗裝對照驗收 (0-ART18/0-QA8)",
        "out_name": "proof_15_chassis_tiger_comparison.png",
        "paints": [
            ("paint_ivory_stock.png", "原廠象牙白 (Ivory Stock)"),
            ("paint_volcano_black.png", "鍛爐淬火曜黑 (Volcano Black)"),
            ("paint_ember_orange.png", "餘燼烈焰暖橘 (Ember Orange)")
        ]
    },
    "crane": {
        "title": "雲嵐鶴 (Crane) Chassis 三款塗裝對照驗收 (含 000e1a9 象牙白)",
        "out_name": "proof_16_chassis_crane_comparison.png",
        "paints": [
            ("paint_ivory_stock.png", "原廠象牙白 (Ivory Stock - 新補齊)"),
            ("paint_zephyr_azure.png", "晴空凌雲湛藍 (Zephyr Azure)"),
            ("paint_crane_porcelain.png", "青花素瓷冷白 (Crane Porcelain)")
        ]
    }
}

def generate_comparisons():
    for d in OUT_DIRS:
        os.makedirs(d, exist_ok=True)

    for race, info in RACES_CHASSIS.items():
        base_dir = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/{race}/chassis"
        card_w = 1200
        card_h = 600
        canvas = Image.new("RGB", (card_w, card_h), (245, 240, 230))
        draw = ImageDraw.Draw(canvas)

        # Title bar
        draw.rectangle([(0, 0), (card_w, 60)], fill=(45, 40, 55))
        draw.text((30, 18), info["title"], fill=(255, 215, 0))

        col_w = card_w // 3
        for idx, (fn, label) in enumerate(info["paints"]):
            fp = os.path.join(base_dir, fn)
            cx = idx * col_w
            # Sub-card background
            draw.rectangle([(cx + 15, 80), (cx + col_w - 15, card_h - 20)], fill=(255, 255, 255), outline=(200, 190, 175), width=2)
            draw.rectangle([(cx + 15, 80), (cx + col_w - 15, 120)], fill=(230, 225, 215))
            draw.text((cx + 25, 92), label, fill=(35, 30, 40))

            if os.path.exists(fp):
                im = Image.open(fp).convert("RGBA")
                # Scale up 3x for clear pixel visual inspection
                scale = 3
                scaled = im.resize((im.width * scale, im.height * scale), Image.Resampling.NEAREST)
                
                # Center horizontally and vertically in card area
                paste_x = cx + (col_w - scaled.width) // 2
                paste_y = 135 + (card_h - 180 - scaled.height) // 2
                
                # Checkboard background for alpha
                cb_size = 12
                for by in range(paste_y, paste_y + scaled.height, cb_size):
                    for bx in range(paste_x, paste_x + scaled.width, cb_size):
                        col = (235, 235, 235) if ((bx // cb_size) + (by // cb_size)) % 2 == 0 else (215, 215, 215)
                        draw.rectangle([(bx, by), (min(bx + cb_size, paste_x + scaled.width), min(by + cb_size, paste_y + scaled.height))], fill=col)

                canvas.paste(scaled, (paste_x, paste_y), scaled)

                # Info footer
                arr = np.array(im)
                opaque = arr[:, :, 3] > 10
                tot_px = int(np.sum(opaque))
                bbox = im.getbbox()
                info_str = f"File: {fn}\nOpaque: {tot_px} px | BBox: {bbox}"
                draw.text((cx + 25, card_h - 65), info_str, fill=(80, 75, 85))
            else:
                draw.text((cx + 30, 250), f"MISSING: {fn}", fill=(200, 40, 40))

        for d in OUT_DIRS:
            out_path = os.path.join(d, info["out_name"])
            canvas.save(out_path, format="PNG")
            print(f"✓ Saved chassis comparison: {out_path}")

if __name__ == "__main__":
    generate_comparisons()
