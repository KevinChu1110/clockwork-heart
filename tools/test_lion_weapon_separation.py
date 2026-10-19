#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
LION_PARTS = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/lion/maple_parts"

body = Image.open(f"{LION_PARTS}/body/paint_brass_gold.png").convert("RGBA")
lance = Image.open(f"{LION_PARTS}/weapon/wpn_knight_lance.png").convert("RGBA")

# 雄獅的 hand 錨點是 (144, 320)，lance origin 是 (69, 293)
# lance 疊加位置是 (144 - 69, 320 - 293) = (75, 27)
comp = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
comp.alpha_composite(body)
comp.alpha_composite(lance, (75, 27))
comp.save("/tmp/lion_weapon_composite_test.png")
print("Saved /tmp/lion_weapon_composite_test.png")
