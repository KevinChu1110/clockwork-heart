import os
from PIL import Image

shot_dir = "/opt/side/bravesoul-game/screenshots"

# 1. fullscreen_comparison
rab_shot = os.path.join(shot_dir, "proof_battle_rabbit.png")
zen_shot = os.path.join(shot_dir, "proof_battle_macaque_equipped_zen_striker.png")

if os.path.exists(rab_shot) and os.path.exists(zen_shot):
    im_r = Image.open(rab_shot).convert("RGBA")
    im_z = Image.open(zen_shot).convert("RGBA")
    w, h = 640, 360
    r_s = im_r.resize((w, h), Image.Resampling.LANCZOS)
    z_s = im_z.resize((w, h), Image.Resampling.LANCZOS)
    c = Image.new("RGBA", (w * 2 + 10, h), (25, 25, 30, 255))
    c.paste(r_s, (0, 0))
    c.paste(z_s, (w + 10, 0))
    out = os.path.join(shot_dir, "proof_battle_rabbit_macaque_fullscreen_comparison.png")
    c.save(out)
    print(f"✓ Updated {out}")

# 2. 390px scale of macaque full screen
fs_shot = os.path.join(shot_dir, "proof_battle_macaque_full_screen.png")
if os.path.exists(fs_shot):
    im_fs = Image.open(fs_shot).convert("RGBA")
    # scale to 390px wide
    h_390 = int(390.0 / im_fs.width * im_fs.height)
    im_390 = im_fs.resize((390, h_390), Image.Resampling.LANCZOS)
    out_390 = os.path.join(shot_dir, "proof_battle_macaque_full_screen_390px.png")
    im_390.save(out_390)
    print(f"✓ Updated {out_390}")
