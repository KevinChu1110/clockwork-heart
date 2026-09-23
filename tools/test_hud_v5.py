#!/usr/bin/env python3
import os
from PIL import Image

pd_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise"
key_512 = Image.open(f"{pd_dir}/winding_key/key_tai_chi_dual_fish_512.png").convert("RGBA")
chassis_512 = Image.open(f"{pd_dir}/chassis/paint_tortoise_jade_512.png").convert("RGBA")
head_512 = Image.open(f"{pd_dir}/head_unit/head_xuanji_tortoise_stock_512.png").convert("RGBA")
costume_512 = Image.open(f"{pd_dir}/costume/costume_zen_dojo_harness_512.png").convert("RGBA")
core_512 = Image.open(f"{pd_dir}/optic_core/core_amber_quartz_512.png").convert("RGBA")

# Build bust composite without weapon / curio clutter
bust_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
bust_512.alpha_composite(key_512)
bust_512.alpha_composite(chassis_512)
bust_512.alpha_composite(head_512)
bust_512.alpha_composite(costume_512)
bust_512.alpha_composite(core_512)

# Crop from upper key y=60 down to bottom of rounded carapace shell y=410, x=50..360
crop = bust_512.crop((50, 60, 360, 410))
cw, ch = crop.size
print("Crop size:", crop.size, "bbox:", crop.getbbox())

target_dim = 100.0
scale = target_dim / max(cw, ch)
sw = int(round(cw * scale))
sh = int(round(ch * scale))
scaled = crop.resize((sw, sh), Image.Resampling.LANCZOS)

hud = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
paste_x = (128 - sw) // 2
paste_y = (128 - sh) // 2
hud.alpha_composite(scaled, (paste_x, paste_y))

hud.save("/tmp/tortoise_hud_v5.png")
print("Saved /tmp/tortoise_hud_v5.png, bbox:", hud.getbbox())
