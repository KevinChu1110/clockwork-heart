#!/usr/bin/env python3
from PIL import Image

MACAQUE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque"

im_ch = Image.open(f"{MACAQUE_DIR}/chassis/paint_ivory_stock_512.png").convert("RGBA")
im_hd = Image.open(f"{MACAQUE_DIR}/head_unit/ear_macaque_coaxial_512.png").convert("RGBA")
im_co = Image.open(f"{MACAQUE_DIR}/costume/costume_dawn_monk_tunic_512.png").convert("RGBA")
im_cr = Image.open(f"{MACAQUE_DIR}/optic_core/core_cyan_emerald_512.png").convert("RGBA")
im_wp = Image.open(f"{MACAQUE_DIR}/weapon/wpn_spring_claws_512.png").convert("RGBA")

comp = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
comp = Image.alpha_composite(comp, im_ch)
comp = Image.alpha_composite(comp, im_hd)
comp = Image.alpha_composite(comp, im_co)
comp = Image.alpha_composite(comp, im_cr)
comp = Image.alpha_composite(comp, im_wp)

comp.save("/tmp/macaque_test/five_512_comp.png")
print("Saved /tmp/macaque_test/five_512_comp.png")
