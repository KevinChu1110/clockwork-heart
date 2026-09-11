import os
from PIL import Image, ImageDraw

POSES_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox"
poses_names = ["idle", "telegraph", "attack", "recover", "skill", "hit"]

sheet = Image.new("RGBA", (128 * 6, 128 + 36), (245, 245, 250, 255))
draw = ImageDraw.Draw(sheet)

heights = {"idle": 109, "telegraph": 102, "attack": 109, "recover": 103, "skill": 109, "hit": 114}

for i, name in enumerate(poses_names):
    im = Image.open(f"{POSES_DIR}/{name}.png")
    sheet.paste(im, (i * 128, 0), im)
    h = heights[name]
    draw.text((i * 128 + 20, 130), f"{name} (h={h})", fill=(30, 30, 45, 255))
    draw.line([(i * 128, 0), (i * 128, 128 + 36)], fill=(210, 210, 220, 255), width=1)
    # Ground reference line at y=117
    draw.line([(i * 128, 117), ((i + 1) * 128, 117)], fill=(255, 60, 60, 100), width=1)

out_p = "/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/proof_fox_combat_six_poses_heights.png"
sheet.save(out_p)
print(f"Saved proof sheet to {out_p}")
