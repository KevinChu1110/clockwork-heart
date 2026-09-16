import subprocess
import os
from PIL import Image

OUT_DIR = "/opt/side/bravesoul-game/proofs/qa_round7"
WS_DIR = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_ac058623/proofs/qa_round7"

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(WS_DIR, exist_ok=True)

# 1. Desktop full/cast screenshot
tmp_desktop = "/tmp/web_desktop_full.png"
subprocess.run([
    "google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu",
    "--window-size=1280,4400", f"--screenshot={tmp_desktop}",
    "file:///opt/side/bravesoul-game/web/index.html"
], check=True)

img_d = Image.open(tmp_desktop)
# The whole page is 1280x4400. Let's crop the #cast section.
# In index.html, #cast starts after hero banner and features (approx y=1400 to y=3300).
# Let's crop cast overview: y from 1350 to 3250
cast_overview = img_d.crop((0, 1380, 1280, 3200))
p1 = os.path.join(OUT_DIR, "proof_01_web_cast_nine_races.png")
cast_overview.save(p1)
cast_overview.save(os.path.join(WS_DIR, "proof_01_web_cast_nine_races.png"))
print("Saved proof_01:", p1, cast_overview.size)

# Detail crop: bottom row with Crane, Bear, Penguin (and Tiger)
# Around y=2300 to y=3200
detail_crop = img_d.crop((0, 2300, 1280, 3200))
p2 = os.path.join(OUT_DIR, "proof_02_web_cast_detail_crane_bear_penguin.png")
detail_crop.save(p2)
detail_crop.save(os.path.join(WS_DIR, "proof_02_web_cast_detail_crane_bear_penguin.png"))
print("Saved proof_02:", p2, detail_crop.size)

# 2. Mobile RWD screenshot
tmp_mobile = "/tmp/web_mobile_full.png"
subprocess.run([
    "google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu",
    "--window-size=420,5200", f"--screenshot={tmp_mobile}",
    "file:///opt/side/bravesoul-game/web/index.html"
], check=True)

img_m = Image.open(tmp_mobile)
# Crop #cast section on mobile (single column stack)
# Let's crop from y=1600 to y=3800
mobile_cast = img_m.crop((0, 1600, 420, 3800))
p3 = os.path.join(OUT_DIR, "proof_03_web_cast_mobile_rwd.png")
mobile_cast.save(p3)
mobile_cast.save(os.path.join(WS_DIR, "proof_03_web_cast_mobile_rwd.png"))
print("Saved proof_03:", p3, mobile_cast.size)
