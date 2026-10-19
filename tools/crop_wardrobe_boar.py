#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_REVIEW = f"{REPO_ROOT}/proofs/eight_races_paperdoll_review/boar"

w_none = Image.open(f"{BOAR_REVIEW}/wardrobe_boar_none_brass_gold.png")
w_harn = Image.open(f"{BOAR_REVIEW}/wardrobe_boar_viking_harness_brass_gold.png")
w_iron = Image.open(f"{BOAR_REVIEW}/wardrobe_boar_viking_ironclad_brass_gold.png")

# 裁出衣櫥中央角色區 (約 300..700, 150..550)
c_none = w_none.crop((350, 150, 650, 550))
c_harn = w_harn.crop((350, 150, 650, 550))
c_iron = w_iron.crop((350, 150, 650, 550))

c_none.save("/tmp/wardrobe_char_none.png")
c_harn.save("/tmp/wardrobe_char_harn.png")
c_iron.save("/tmp/wardrobe_char_iron.png")
print("Saved wardrobe character crops to /tmp")
