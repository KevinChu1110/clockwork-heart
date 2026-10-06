from PIL import Image
import os

# 尋找白兔組合貼圖或 showcase 圖
paths = [
    "game/assets/sprites/player/paperdoll/rabbit/composite_idle_512.png",
    "game/assets/sprites/characters/rabbit_showcase_hd.png",
    "game/assets/sprites/characters/rabbit_idle.png"
]
for p in paths:
    if os.path.exists(p):
        im = Image.open(p)
        bbox = im.getbbox()
        print(p, "size:", im.size, "bbox:", bbox)
