#!/usr/bin/env python3
from PIL import Image

head_512 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise/head_unit/head_xuanji_tortoise_stock_512.png").convert("RGBA")
chassis_512 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise/chassis/paint_tortoise_jade_512.png").convert("RGBA")

# Composite just chassis upper collar and head
head_full = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
# Neck collar from chassis in region x in [180..340], y in [160..245]
collar_mask = Image.new("L", (512, 512), 0)
for y in range(170, 245):
    for x in range(195, 315):
        collar_mask.putpixel((x, y), 255)

head_full.paste(chassis_512, (0, 0), collar_mask)
head_full.alpha_composite(head_512)

# Crop head_full
hb = head_full.getbbox()
print("Clean head bbox:", hb)
assert hb is not None
head_crop = head_full.crop(hb)
hw, hh = head_crop.size

# Target: 96px inside 128x128
target_dim = 96.0
scale = target_dim / max(hw, hh)
scaled_w = int(round(hw * scale))
scaled_h = int(round(hh * scale))
scaled_head = head_crop.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)

hud_img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
hud_img.alpha_composite(scaled_head, ((128 - scaled_w) // 2, (128 - scaled_h) // 2))

hud_img.save("/tmp/clean_hud_tortoise.png")
print("Saved /tmp/clean_hud_tortoise.png, bbox:", hud_img.getbbox())
