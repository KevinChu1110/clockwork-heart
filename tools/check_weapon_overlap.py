import os
from PIL import Image

repo = "/opt/side/bravesoul-game"
paperdoll = f"{repo}/game/assets/sprites/player/paperdoll"

for race in ["rabbit", "lion", "fox", "boar", "macaque"]:
    wpn_p = f"{paperdoll}/{race}/weapon"
    ch_p = f"{paperdoll}/{race}/chassis/paint_ivory_stock.png"
    wpn_files = [f for f in os.listdir(wpn_p) if f.endswith(".png") and not f.endswith(".import")]
    if not wpn_files:
        continue
    w_im = Image.open(f"{wpn_p}/{wpn_files[0]}").convert("RGBA")
    c_im = Image.open(ch_p).convert("RGBA")
    
    # Check overlap pixels where both w_im and c_im have alpha > 128
    w_data = w_im.load()
    c_data = c_im.load()
    overlap = 0
    for y in range(128):
        for x in range(128):
            if w_data[x, y][3] > 128 and c_data[x, y][3] > 128:
                overlap += 1
    print(f"{race}: weapon={wpn_files[0]}, overlap with chassis={overlap} pixels")
