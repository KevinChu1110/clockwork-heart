#!/usr/bin/env python3
from PIL import Image

pd_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise"
key_512 = Image.open(f"{pd_dir}/winding_key/key_tai_chi_dual_fish_512.png").convert("RGBA")
curio_512 = Image.open(f"{pd_dir}/back_curio/curio_bagua_armillary_rings_512.png").convert("RGBA")
chassis_512 = Image.open(f"{pd_dir}/chassis/paint_tortoise_jade_512.png").convert("RGBA")
head_512 = Image.open(f"{pd_dir}/head_unit/head_xuanji_tortoise_stock_512.png").convert("RGBA")
costume_512 = Image.open(f"{pd_dir}/costume/costume_zen_dojo_harness_512.png").convert("RGBA")
core_512 = Image.open(f"{pd_dir}/optic_core/core_amber_quartz_512.png").convert("RGBA")
weapon_512 = Image.open(f"{pd_dir}/weapon/wpn_bagua_astrolabe_512.png").convert("RGBA")

# Build focused dialogue bust
bust = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
bust.alpha_composite(key_512)
bust.paste(curio_512, (15, 0), curio_512)
bust.alpha_composite(chassis_512)
bust.alpha_composite(head_512)
bust.alpha_composite(costume_512)
bust.alpha_composite(core_512)
bust.paste(weapon_512, (-25, -10), weapon_512)

# Crop from top of key y=55 down to waistline y=355 (cleanly cutting across mid-torso, 0 legs/feet)
crop = bust.crop((45, 55, 425, 355))
cw, ch = crop.size
print("Crop size:", crop.size)

target_w = 364.0
scale = target_w / cw
sw = int(round(cw * scale))
sh = int(round(ch * scale))
scaled = crop.resize((sw, sh), Image.Resampling.LANCZOS)

dialogue_bust = Image.new("RGBA", (384, 480), (0, 0, 0, 0))
paste_x = (384 - sw) // 2
paste_y = 480 - sh
dialogue_bust.alpha_composite(scaled, (paste_x, paste_y))

dialogue_bust.save("/tmp/test_dialogue_bust_perfect3.png")
print("Saved /tmp/test_dialogue_bust_perfect3.png, bbox:", dialogue_bust.getbbox())
