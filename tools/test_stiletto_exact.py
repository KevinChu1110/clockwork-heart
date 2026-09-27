from PIL import Image, ImageChops
import numpy as np

BASE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/cat"
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_cat_shadowspring_stiletto.png").convert("RGBA")
wpn_bbox = weapon_src.getbbox()
scepter_raw = weapon_src.crop(wpn_bbox)

out = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
out.paste(scepter_raw, (wpn_bbox[0], wpn_bbox[1]))
diff = ImageChops.difference(out, weapon_src)
print("Exact placement diff bbox:", diff.getbbox())
