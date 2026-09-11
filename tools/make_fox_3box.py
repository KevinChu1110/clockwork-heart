import os
from PIL import Image

idle_im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/idle.png").convert("RGBA")
battle_im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/fox_battle.png").convert("RGBA")
cand_im = Image.open("/tmp/test_attack_candidate_v2.png").convert("RGBA")

box_size = 48
half = box_size // 2

# Center for idle: (61, 46)
crop_idle = idle_im.crop((61 - half, 46 - half, 61 + half, 46 + half))

# Center for battle: (68, 59)
crop_battle = battle_im.crop((68 - half, 59 - half, 68 + half, 59 + half))

# Center for candidate attack: (78, 47)
crop_cand = cand_im.crop((78 - half, 47 - half, 78 + half, 47 + half))

pad = 8
sheet = Image.new("RGBA", (box_size * 3 + pad * 4, box_size + pad * 2), (240, 240, 240, 255))
sheet.paste(crop_idle, (pad, pad))
sheet.paste(crop_battle, (pad * 2 + box_size, pad))
sheet.paste(crop_cand, (pad * 3 + box_size * 2, pad))

sheet.save("/tmp/fox_head_3box_1x.png")
sheet_4x = sheet.resize((sheet.width * 4, sheet.height * 4), Image.Resampling.NEAREST)
sheet_4x.save("/tmp/fox_head_3box_4x.png")
print("Saved /tmp/fox_head_3box_1x.png and /tmp/fox_head_3box_4x.png with candidate_v2")
