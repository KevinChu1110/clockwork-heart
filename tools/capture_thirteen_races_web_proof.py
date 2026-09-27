import os
import subprocess
from PIL import Image

OUT_DIR = "/opt/side/bravesoul-game/proofs/web_thirteen_races"
os.makedirs(OUT_DIR, exist_ok=True)

tmp_desktop = "/tmp/web_desktop_full_thirteen.png"
subprocess.run([
    "google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu",
    "--window-size=1280,6800", f"--screenshot={tmp_desktop}",
    "file:///opt/side/bravesoul-game/web/index.html"
], check=True)

im = Image.open(tmp_desktop)
print("Desktop screenshot size:", im.size)

# The #cast section contains header and the 13 races showcase.
# Let's crop the whole cast section
# Usually starting around y=1800 to y=5200 with 13 cards (5 rows of 3 cols)
proof_cast = im.crop((0, 1800, 1280, 5200))
cast_path = os.path.join(OUT_DIR, "proof_web_cast_thirteen_races.png")
proof_cast.save(cast_path)
print("Saved:", cast_path, proof_cast.size)

# Detail crop focusing on the bottom rows: Tortoise, Elephant, Frog, Panda
# From around y=3600 to y=5200
detail_crop = im.crop((0, 3400, 1280, 5200))
detail_path = os.path.join(OUT_DIR, "proof_web_new_races_detail.png")
detail_crop.save(detail_path)
print("Saved:", detail_path, detail_crop.size)

# Mobile screenshot 390px
tmp_mobile = "/tmp/web_mobile_full_thirteen.png"
subprocess.run([
    "google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu",
    "--window-size=390,13000", f"--screenshot={tmp_mobile}",
    "file:///opt/side/bravesoul-game/web/index.html"
], check=True)

im_m = Image.open(tmp_mobile)
print("Mobile screenshot size:", im_m.size)
# Save mobile section containing elephant, frog, panda cards (at the bottom of races grid)
mobile_crop = im_m.crop((0, 8000, 390, 11500))
mobile_path = os.path.join(OUT_DIR, "proof_web_mobile_new_races.png")
mobile_crop.save(mobile_path)
print("Saved:", mobile_path, mobile_crop.size)
