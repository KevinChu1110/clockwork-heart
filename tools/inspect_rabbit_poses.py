import os
from PIL import Image, ImageChops

base_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/poses"
idle = Image.open(f"{base_dir}/idle.png").convert("RGBA")
poses = ["attack", "hit", "idle", "recover", "skill", "telegraph"]

for p in poses:
    img = Image.open(f"{base_dir}/{p}.png").convert("RGBA")
    diff = ImageChops.difference(idle, img)
    bbox = diff.getbbox()
    diff_data = list(diff.convert("L").getdata())
    diff_px = sum(1 for x in diff_data if x > 10)
    print(f"rabbit {p}: size={img.size}, bbox={img.getbbox()}, diff_from_idle_bbox={bbox}, diff_pixels={diff_px}")
