#!/usr/bin/env python3
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/proofs/qa_round28/proof_02_creation_elephant_fortress.png")
print("Size:", im.size)
# In creation mode, let's find the bbox of the stage or check where the stage is located in paperdoll_select_demo.tscn
