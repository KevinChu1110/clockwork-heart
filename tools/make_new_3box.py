#!/usr/bin/env python3
import sys
sys.path.insert(0, "/opt/side/bravesoul-game/tools")
from typing import cast
from PIL import Image
from test_new_striker import create_candidate

cand = create_candidate()
# Trim x > 68
cand_trimmed = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
for y in range(128):
    for x in range(128):
        if x > 68:
            continue
        col = cast(tuple[int,int,int,int], cand.getpixel((x, y)))
        if col[3] > 0:
            cand_trimmed.putpixel((x, y), col)

MACAQUE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque"

def get_slot_layer(slot: str, fn: str) -> Image.Image:
    p = f"{MACAQUE_DIR}/{slot}/{fn}"
    return Image.open(p).convert("RGBA")

def build_comp_with_costume(cos_img: Image.Image | None):
    comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    comp.alpha_composite(get_slot_layer("winding_key", "key_classic_brass.png"))
    comp.alpha_composite(get_slot_layer("back_curio", "curio_spring_tail.png"))
    comp.alpha_composite(get_slot_layer("chassis", "paint_ivory_stock.png"))
    comp.alpha_composite(get_slot_layer("head_unit", "ear_macaque_coaxial.png"))
    if cos_img is not None:
        comp.alpha_composite(cos_img)
    comp.alpha_composite(get_slot_layer("optic_core", "core_cyan_emerald.png"))
    comp.alpha_composite(get_slot_layer("weapon", "wpn_spring_claws.png"))
    return comp

c_bare = build_comp_with_costume(None)
tunic_img = Image.open(f"{MACAQUE_DIR}/costume/costume_dawn_monk_tunic.png").convert("RGBA")
c_tunic = build_comp_with_costume(tunic_img)
c_new_zen = build_comp_with_costume(cand_trimmed)

# Crop 30,38-100,86
b_crop = c_bare.crop((30, 38, 100, 86))
t_crop = c_tunic.crop((30, 38, 100, 86))
z_crop = c_new_zen.crop((30, 38, 100, 86))

w, h = b_crop.size
combined = Image.new("RGBA", (w * 3 + 20, h), (30, 30, 30, 255))
combined.paste(b_crop, (0, 0))
combined.paste(t_crop, (w + 10, 0))
combined.paste(z_crop, (w * 2 + 20, 0))

combined_14x = combined.resize((combined.width * 14, combined.height * 14), Image.Resampling.NEAREST)
combined_14x.save("/opt/side/bravesoul-game/screenshots/test_new_3box_check.png")
print("Saved /opt/side/bravesoul-game/screenshots/test_new_3box_check.png")
