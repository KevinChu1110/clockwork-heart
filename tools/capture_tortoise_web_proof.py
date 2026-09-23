import os
import subprocess
from PIL import Image

OUT_DIR = "/opt/side/bravesoul-game/proofs/web_tortoise"
os.makedirs(OUT_DIR, exist_ok=True)

tmp_desktop = "/tmp/web_desktop_full_tortoise.png"
subprocess.run([
    "google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu",
    "--window-size=1280,5500", f"--screenshot={tmp_desktop}",
    "file:///opt/side/bravesoul-game/web/index.html"
], check=True)

im = Image.open(tmp_desktop)
print("Desktop screenshot size:", im.size)

# Let's save the full desktop screenshot or cropped #cast section
# We can find the cast section or crop from y=1800 to y=4200 (which covers the 10 races showcase)
# Let's check where the races showcase is located
proof_cast = im.crop((0, 1800, 1280, 4200))
cast_path = os.path.join(OUT_DIR, "proof_web_cast_ten_races.png")
proof_cast.save(cast_path)
print("Saved:", cast_path, proof_cast.size)

# Detail crop focusing on the bottom rows: Bear, Penguin, and Tortoise (玄機龜)
# Around y=2800 to y=4200
detail_crop = im.crop((0, 2700, 1280, 4200))
detail_path = os.path.join(OUT_DIR, "proof_web_tortoise_card_detail.png")
detail_crop.save(detail_path)
print("Saved:", detail_path, detail_crop.size)

# Mobile screenshot 390px
tmp_mobile = "/tmp/web_mobile_full_tortoise.png"
subprocess.run([
    "google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu",
    "--window-size=390,9500", f"--screenshot={tmp_mobile}",
    "file:///opt/side/bravesoul-game/web/index.html"
], check=True)

im_m = Image.open(tmp_mobile)
print("Mobile screenshot size:", im_m.size)
# Save mobile bottom containing tortoise card
mobile_tortoise = im_m.crop((0, 6000, 390, 8500))
mobile_path = os.path.join(OUT_DIR, "proof_web_mobile_tortoise.png")
mobile_tortoise.save(mobile_path)
print("Saved:", mobile_path, mobile_tortoise.size)
