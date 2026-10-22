#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"

slots = [
    ("winding_key", "key_classic_brass.png"),
    ("back_curio", "curio_spring_tail.png"),
    ("chassis", "paint_ivory_stock.png"),
    ("head_unit", "ear_macaque_coaxial.png"),
    ("costume", "costume_dawn_monk_tunic.png"),
    ("optic_core", "core_cyan_emerald.png"),
    ("weapon", "wpn_spring_claws.png"),
]

comp512_pixel = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
for slot, fn in slots:
    p = f"{MACAQUE_DIR}/{slot}/{fn}"
    layer = Image.open(p).convert("RGBA")
    layer512 = layer.resize((512, 512), Image.Resampling.NEAREST)
    comp512_pixel = Image.alpha_composite(comp512_pixel, layer512)

comp512_pixel.save("/tmp/macaque_test/pixel_512_comp.png")
print("Saved /tmp/macaque_test/pixel_512_comp.png")
