import os
from PIL import Image

repo = "/opt/side/bravesoul-game"
paperdoll = f"{repo}/game/assets/sprites/player/paperdoll"

for race in ["lion", "fox", "boar", "macaque"]:
    proof_p = f"{paperdoll}/{race}/proof_paperdoll_{race}_composite.png"
    if os.path.exists(proof_p):
        im = Image.open(proof_p).convert("RGBA")
        im.resize((512, 512), getattr(Image, 'Resampling', Image).NEAREST).save(f"/tmp/proof_{race}_4x.png")
        print(f"Saved {race} proof 4x")
