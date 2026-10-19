#!/usr/bin/env python3
from PIL import Image

lion_core = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/lion/optic_core/core_cyan_emerald_512.png").convert("RGBA")

# 雄獅的額頭在 y < 200，胸口在 y > 250！
orb1 = lion_core.crop((215, 160, 270, 215)) # 額頭
orb2 = lion_core.crop((185, 260, 270, 320)) # 胸口！

orb1.save("/tmp/lion_orb_forehead.png")
orb2.save("/tmp/lion_orb_chest.png")
print("Saved lion_orb_forehead.png and lion_orb_chest.png")
