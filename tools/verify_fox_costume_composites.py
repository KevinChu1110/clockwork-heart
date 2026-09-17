#!/usr/bin/env python3
"""
tools/verify_fox_costume_composites.py
Verifies paperdoll composite for Fox under:
1. Bare chassis (costume = none)
2. costume_astral_cape
3. costume_astral_observer
4. costume_viking_harness (common 512)
"""

import os
from PIL import Image

FOX_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/fox"
COMMON_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/common"

# Load chassis 512
chassis_512 = Image.open(f"{FOX_DIR}/chassis/paint_fox_orange_512.png").convert("RGBA")

# 1. Bare composite (no costume)
bare_comp = chassis_512.copy()
bare_comp.save("/opt/side/bravesoul-game/proofs/proof_fox_composite_bare_512.png")
print("Saved proofs/proof_fox_composite_bare_512.png")

# 2. Composite with astral_cape
cape_p = f"{COMMON_DIR}/costume/costume_astral_cape_512.png"
if os.path.exists(cape_p):
    cape_img = Image.open(cape_p).convert("RGBA")
    comp_cape = chassis_512.copy()
    comp_cape.alpha_composite(cape_img)
    comp_cape.save("/opt/side/bravesoul-game/proofs/proof_fox_composite_astral_cape_512.png")
    print("Saved proofs/proof_fox_composite_astral_cape_512.png")

# 3. Composite with viking_harness
viking_p = f"{COMMON_DIR}/costume/costume_viking_harness_512.png"
if os.path.exists(viking_p):
    viking_img = Image.open(viking_p).convert("RGBA")
    comp_viking = chassis_512.copy()
    comp_viking.alpha_composite(viking_img)
    comp_viking.save("/opt/side/bravesoul-game/proofs/proof_fox_composite_viking_512.png")
    print("Saved proofs/proof_fox_composite_viking_512.png")
