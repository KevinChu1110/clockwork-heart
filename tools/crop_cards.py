import os
from PIL import Image

im = Image.open("/tmp/test_http_1280.png")
OUT_DIR = "/opt/side/bravesoul-game/proofs/web_thirteen_races"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. 鋼岳象 card
crop_elephant = im.crop((440, 3830, 835, 4460))
path_elephant = os.path.join(OUT_DIR, "proof_card_elephant.png")
crop_elephant.save(path_elephant)
print("Saved elephant card:", path_elephant, crop_elephant.size)

# 2. 碧簧蛙 card
crop_frog = im.crop((840, 3830, 1235, 4460))
path_frog = os.path.join(OUT_DIR, "proof_card_frog.png")
crop_frog.save(path_frog)
print("Saved frog card:", path_frog, crop_frog.size)

# 3. 瓷韻熊貓 card
crop_panda = im.crop((40, 4475, 435, 5105))
path_panda = os.path.join(OUT_DIR, "proof_card_panda.png")
crop_panda.save(path_panda)
print("Saved panda card:", path_panda, crop_panda.size)

# 4. 玄機龜 card for reference
crop_tortoise = im.crop((40, 3830, 435, 4460))
path_tortoise = os.path.join(OUT_DIR, "proof_card_tortoise.png")
crop_tortoise.save(path_tortoise)
print("Saved tortoise card:", path_tortoise, crop_tortoise.size)
