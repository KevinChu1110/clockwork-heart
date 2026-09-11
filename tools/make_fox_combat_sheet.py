import os
from PIL import Image, ImageDraw, ImageFont

POSES_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox"
poses_names = ["idle", "telegraph", "attack", "recover", "skill", "hit"]

sheet = Image.new("RGBA", (128 * 6, 128 + 24), (240, 240, 245, 255))
draw = ImageDraw.Draw(sheet)

for i, name in enumerate(poses_names):
    if name == "recover":
        im = Image.open("/tmp/fox_test/new_recover.png")
    elif name == "skill":
        im = Image.open("/tmp/fox_test/new_skill.png")
    else:
        im = Image.open(f"{POSES_DIR}/{name}.png")
    
    sheet.paste(im, (i * 128, 0), im)
    draw.text((i * 128 + 35, 130), name, fill=(30, 30, 40, 255))
    draw.line([(i * 128, 0), (i * 128, 128 + 24)], fill=(200, 200, 210, 255), width=1)
    # Ground line reference at y=117
    draw.line([(i * 128, 117), ((i + 1) * 128, 117)], fill=(255, 0, 0, 80), width=1)

out_p = "/tmp/fox_test/fox_six_poses_sheet.png"
sheet.save(out_p)
print(f"Saved contact sheet to {out_p}")
