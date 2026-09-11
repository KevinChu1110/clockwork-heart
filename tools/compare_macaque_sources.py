#!/usr/bin/env python3
from PIL import Image

char_m = Image.open("/opt/side/bravesoul-game/branding/char_macaque.png")
print("char_macaque size:", char_m.size)
ivory = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png")
print("paint_ivory_stock size:", ivory.size)
comp = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/proof_paperdoll_macaque_composite.png")
print("composite size:", comp.size)
m_battle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/macaque_battle.png")
print("macaque_battle size:", m_battle.size)
