#!/usr/bin/env python3
"""
tools/make_penguin_comparison_8x.py
Generates an 8x scaled comparison board on magenta:
Left: head_unit (head_steam_penguin_stock.png)
Middle: first costume (costume_navigator_harness.png)
Right: new second costume (costume_abyssal_diver_cuirass.png)
All cropped to their bbox and placed side by side.
"""

from PIL import Image, ImageDraw

REPO_ROOT = "/opt/side/bravesoul-game"
PENGUIN_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/penguin"

def make_board(out_path="/tmp/penguin_costume_comparison_8x.png"):
    p_head = f"{PENGUIN_DIR}/head_unit/head_steam_penguin_stock.png"
    p_c1 = f"{PENGUIN_DIR}/costume/costume_navigator_harness.png"
    p_c2 = f"{PENGUIN_DIR}/costume/costume_abyssal_diver_cuirass.png"

    im_head = Image.open(p_head).convert("RGBA")
    im_c1 = Image.open(p_c1).convert("RGBA")
    im_c2 = Image.open(p_c2).convert("RGBA")

    # Crop to bbox
    crop_head = im_head.crop(im_head.getbbox())
    crop_c1 = im_c1.crop(im_c1.getbbox())
    crop_c2 = im_c2.crop(im_c2.getbbox())

    SCALE = 8
    def scale_and_magenta(im):
        w, h = im.size
        large = im.resize((w * SCALE, h * SCALE), Image.Resampling.NEAREST)
        mag = Image.new("RGBA", large.size, (255, 0, 255, 255))
        mag.alpha_composite(large)
        return mag

    m_head = scale_and_magenta(crop_head)
    m_c1 = scale_and_magenta(crop_c1)
    m_c2 = scale_and_magenta(crop_c2)

    pad = 20
    header = 50
    total_w = pad + m_head.width + pad + m_c1.width + pad + m_c2.width + pad
    max_h = max(m_head.height, m_c1.height, m_c2.height)
    total_h = header + max_h + pad

    board = Image.new("RGBA", (total_w, total_h), (25, 20, 35, 255))
    d = ImageDraw.Draw(board)

    # Paste
    curr_x = pad
    # 1. Head
    d.text((curr_x, 15), "1. Head Unit Stock (Ref)", fill=(255, 220, 80, 255))
    board.paste(m_head, (curr_x, header))
    curr_x += m_head.width + pad

    # 2. Costume 1
    d.text((curr_x, 15), "2. Costume 1 Navigator (Ref)", fill=(255, 220, 80, 255))
    board.paste(m_c1, (curr_x, header))
    curr_x += m_c1.width + pad

    # 3. Costume 2
    d.text((curr_x, 15), "3. Costume 2 Abyssal (New)", fill=(255, 220, 80, 255))
    board.paste(m_c2, (curr_x, header))

    board.save(out_path)
    print(f"✓ Saved 8x comparison board: {out_path} ({total_w}x{total_h})")
    return out_path

if __name__ == "__main__":
    make_board()
