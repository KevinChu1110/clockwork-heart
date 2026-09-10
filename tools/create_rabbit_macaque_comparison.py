#!/usr/bin/env python3
"""
tools/create_rabbit_macaque_comparison.py
Creates side-by-side comparison of Rabbit and Macaque:
1. Full battle view side-by-side (Rabbit vs Macaque Zen Striker vs Dawn Monk)
2. Character close-up side-by-side
3. Reviewer standard 8x NEAREST zoom comparison on Magenta background
"""

import os
from PIL import Image

shot_dir = "/opt/side/bravesoul-game/screenshots"
macaque_chassis_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis"
rabbit_chassis_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit/chassis"

rab_shot = os.path.join(shot_dir, "proof_battle_rabbit.png")
zen_shot = os.path.join(shot_dir, "proof_battle_macaque_equipped_zen_striker.png")
dawn_shot = os.path.join(shot_dir, "proof_battle_macaque_equipped_dawn_monk.png")

def make_comparisons():
    if os.path.exists(rab_shot) and os.path.exists(zen_shot) and os.path.exists(dawn_shot):
        im_rab = Image.open(rab_shot).convert("RGBA")
        im_zen = Image.open(zen_shot).convert("RGBA")
        im_dawn = Image.open(dawn_shot).convert("RGBA")
        
        # 1. Fullscreen comparison
        w, h = 640, 360
        r_s = im_rab.resize((w, h), Image.Resampling.LANCZOS)
        z_s = im_zen.resize((w, h), Image.Resampling.LANCZOS)
        d_s = im_dawn.resize((w, h), Image.Resampling.LANCZOS)
        
        comp_full = Image.new("RGBA", (w * 2 + 10, h), (25, 25, 30, 255))
        comp_full.paste(r_s, (0, 0))
        comp_full.paste(z_s, (w + 10, 0))
        out_full = os.path.join(shot_dir, "proof_battle_rabbit_macaque_comparison.png")
        comp_full.save(out_full)
        print(f"✓ Saved {out_full}")
        
        # 2. Characters crop comparison
        crop_box = (200, 180, 580, 660)
        c_r = im_rab.crop(crop_box)
        c_d = im_dawn.crop(crop_box)
        c_z = im_zen.crop(crop_box)
        cw, ch = c_r.size
        
        comp_chars = Image.new("RGBA", (cw * 3 + 20, ch), (25, 25, 30, 255))
        comp_chars.paste(c_r, (0, 0))
        comp_chars.paste(c_d, (cw + 10, 0))
        comp_chars.paste(c_z, (cw * 2 + 20, 0))
        out_chars = os.path.join(shot_dir, "proof_battle_rabbit_macaque_characters_comparison.png")
        comp_chars.save(out_chars)
        print(f"✓ Saved {out_chars}")
        
    # 3. 8x zoom on Magenta comparison (Review standard)
    mac_iv = os.path.join(macaque_chassis_dir, "paint_ivory_stock.png")
    rab_iv = os.path.join(rabbit_chassis_dir, "paint_ivory_stock.png")
    if os.path.exists(mac_iv) and os.path.exists(rab_iv):
        im_m = Image.open(mac_iv).convert("RGBA")
        im_r = Image.open(rab_iv).convert("RGBA")
        im_m_8x = im_m.resize((im_m.width * 8, im_m.height * 8), Image.Resampling.NEAREST)
        im_r_8x = im_r.resize((im_r.width * 8, im_r.height * 8), Image.Resampling.NEAREST)
        
        W = im_m_8x.width + im_r_8x.width + 20
        H = max(im_m_8x.height, im_r_8x.height)
        comp_8x = Image.new("RGBA", (W, H), (255, 0, 255, 255))
        comp_8x.paste(im_m_8x, (0, 0), im_m_8x)
        comp_8x.paste(im_r_8x, (im_m_8x.width + 20, 0), im_r_8x)
        out_8x = os.path.join(shot_dir, "proof_chassis_8x_comparison.png")
        comp_8x.convert("RGB").save(out_8x)
        print(f"✓ Saved {out_8x}")

if __name__ == "__main__":
    make_comparisons()
