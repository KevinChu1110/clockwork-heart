import sys
sys.path.insert(0, '/opt/side/bravesoul-game')
from PIL import Image
from tools.generate_macaque_proofs import build_composite

c_dawn = build_composite("paint_ivory_stock.png", "costume_dawn_monk_tunic.png")
c_zen = build_composite("paint_bamboo_bronze.png", "costume_zen_striker.png")

c_dawn.save("/tmp/macaque_composite_dawn.png")
c_zen.save("/tmp/macaque_composite_zen.png")

# Zoom 8x on white background
for name, comp in [("dawn", c_dawn), ("zen", c_zen)]:
    z = comp.resize((comp.width * 8, comp.height * 8), Image.Resampling.NEAREST)
    bg = Image.new("RGBA", z.size, (255, 255, 255, 255))
    bg.alpha_composite(z)
    bg.convert("RGB").save(f"/tmp/macaque_{name}_8x_white.png")
    print(f"Saved /tmp/macaque_{name}_8x_white.png")
