#!/usr/bin/env python3
import sys, os
sys.path.insert(0, "/opt/side/bravesoul-game/tools")
from PIL import Image
from generate_macaque_proofs import build_composite

os.makedirs("/opt/side/bravesoul-game/screenshots", exist_ok=True)

c_bare = build_composite("paint_ivory_stock.png", None)
c_tunic = build_composite("paint_ivory_stock.png", "costume_dawn_monk_tunic.png")
c_zen = build_composite("paint_ivory_stock.png", "costume_zen_striker.png")

# Crop 30,38-100,86
b_crop = c_bare.crop((30, 38, 100, 86))
t_crop = c_tunic.crop((30, 38, 100, 86))
z_crop = c_zen.crop((30, 38, 100, 86))

w, h = b_crop.size
combined = Image.new("RGBA", (w * 3 + 20, h), (30, 30, 30, 255))
combined.paste(b_crop, (0, 0))
combined.paste(t_crop, (w + 10, 0))
combined.paste(z_crop, (w * 2 + 20, 0))

combined_14x = combined.resize((combined.width * 14, combined.height * 14), Image.Resampling.NEAREST)
combined_14x.save("/opt/side/bravesoul-game/screenshots/current_3box_check.png")
print("Saved /opt/side/bravesoul-game/screenshots/current_3box_check.png")
