#!/usr/bin/env python3
from PIL import Image

pd_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise"
slices_512 = [
    f"{pd_dir}/winding_key/key_tai_chi_dual_fish_512.png",
    f"{pd_dir}/back_curio/curio_bagua_armillary_rings_512.png",
    f"{pd_dir}/chassis/paint_tortoise_jade_512.png",
    f"{pd_dir}/head_unit/head_xuanji_tortoise_stock_512.png",
    f"{pd_dir}/costume/costume_zen_dojo_harness_512.png",
    f"{pd_dir}/optic_core/core_amber_quartz_512.png",
    f"{pd_dir}/weapon/wpn_bagua_astrolabe_512.png",
]
comp512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
for p in slices_512:
    comp512.alpha_composite(Image.open(p).convert("RGBA"))

# Crop from y=55 down to y=455 (upper legs / thighs), x=25..465 (width 440, height 400)
bust_crop = comp512.crop((25, 55, 465, 455))
bw, bh = bust_crop.size

scale = 368.0 / bw
scaled_w = int(round(bw * scale))
scaled_h = int(round(bh * scale))

scaled_bust = bust_crop.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
dialogue_bust = Image.new("RGBA", (384, 480), (0, 0, 0, 0))
paste_x = (384 - scaled_w) // 2
paste_y = 480 - scaled_h
dialogue_bust.alpha_composite(scaled_bust, (paste_x, paste_y))

dialogue_bust.save("/tmp/test_dialogue_bust_scaled.png")
print("Bbox:", dialogue_bust.getbbox(), "height:", scaled_h, "top:", paste_y)
