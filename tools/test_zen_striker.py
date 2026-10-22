#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"

# 看看裸體 chassis + head + key + tail:
im_ch = Image.open(f"{MACAQUE_DIR}/chassis/paint_ivory_stock.png").convert("RGBA")
im_hd = Image.open(f"{MACAQUE_DIR}/head_unit/ear_macaque_coaxial.png").convert("RGBA")
im_ky = Image.open(f"{MACAQUE_DIR}/winding_key/key_classic_brass.png").convert("RGBA")
im_tl = Image.open(f"{MACAQUE_DIR}/back_curio/curio_spring_tail.png").convert("RGBA")
im_zen = Image.open(f"{MACAQUE_DIR}/costume/costume_zen_striker.png").convert("RGBA")

# 1. 純淨素體合成 (Bare)
bare = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
bare = Image.alpha_composite(bare, im_ky)
bare = Image.alpha_composite(bare, im_tl)
bare = Image.alpha_composite(bare, im_ch)
bare = Image.alpha_composite(bare, im_hd)
bare.save("/tmp/macaque_test/macaque_bare.png")

# 2. 穿 zen striker
comp_zen = Image.alpha_composite(bare.copy(), im_zen)
comp_zen.save("/tmp/macaque_test/macaque_zen.png")

print("Saved macaque_bare.png and macaque_zen.png")
