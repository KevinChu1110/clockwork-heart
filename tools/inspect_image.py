import os
from PIL import Image

for path in [
    "/tmp/web_desktop_full_thirteen.png",
    "/opt/side/bravesoul-game/proofs/web_thirteen_races/proof_web_cast_thirteen_races.png",
    "/opt/side/bravesoul-game/proofs/web_thirteen_races/proof_web_new_races_detail.png"
]:
    if os.path.exists(path):
        im = Image.open(path)
        bbox = im.getbbox()
        extrema = im.getextrema()
        print(f"{path}: size={im.size}, mode={im.mode}, bbox={bbox}")
