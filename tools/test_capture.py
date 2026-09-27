import os
import time
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

def run_server():
    os.chdir("/opt/side/bravesoul-game/web")
    server = HTTPServer(("127.0.0.1", 8999), QuietHandler)
    server.serve_forever()

t = threading.Thread(target=run_server, daemon=True)
t.start()
time.sleep(1)

out_png = "/tmp/test_http_1280.png"
subprocess.run([
    "google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu",
    "--virtual-time-budget=5000",
    "--run-all-compositor-stages-before-draw",
    "--window-size=1280,6800",
    f"--screenshot={out_png}",
    "http://127.0.0.1:8999/index.html"
], check=True)

from PIL import Image
im = Image.open(out_png)
print("Captured HTTP screenshot size:", im.size)

# Crop races showcase
# From card tops: 1902 to 5102
# Let's crop cards area from y=1800 to y=5250
races_crop = im.crop((0, 1800, 1280, 5250))
races_path = "/opt/side/bravesoul-game/proofs/web_thirteen_races/proof_web_all_thirteen_races.png"
races_crop.save(races_path)
print("Saved all 13 races proof:", races_path, races_crop.size)

# Detail crop of row 4 (Tortoise, Elephant, Frog) and row 5 (Panda)
# y=3750 to y=5250 (height 1500)
new_crop = im.crop((0, 3750, 1280, 5250))
new_path = "/opt/side/bravesoul-game/proofs/web_thirteen_races/proof_web_new_races_detail.png"
new_crop.save(new_path)
print("Saved new races detail proof:", new_path, new_crop.size)

# Mobile 390px
out_mobile = "/tmp/test_http_390.png"
subprocess.run([
    "google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu",
    "--virtual-time-budget=5000",
    "--run-all-compositor-stages-before-draw",
    "--window-size=390,13000",
    f"--screenshot={out_mobile}",
    "http://127.0.0.1:8999/index.html"
], check=True)

im_m = Image.open(out_mobile)
print("Captured mobile HTTP screenshot size:", im_m.size)
# In mobile, 13 cards are stacked vertically.
# Let's crop the bottom cards (Tortoise, Elephant, Frog, Panda)
# Let's crop from y=8500 to y=12500
mobile_crop = im_m.crop((0, 8500, 390, 12500))
mobile_path = "/opt/side/bravesoul-game/proofs/web_thirteen_races/proof_web_mobile_new_races.png"
mobile_crop.save(mobile_path)
print("Saved mobile new races proof:", mobile_path, mobile_crop.size)
