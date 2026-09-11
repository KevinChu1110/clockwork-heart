import glob
from PIL import Image

for p in sorted(glob.glob("game/assets/sprites/player/paperdoll/rabbit/*/*.png")):
    im = Image.open(p).convert("RGBA")
    print(f"{p:70s} size={im.size} bbox={im.getbbox()}")
