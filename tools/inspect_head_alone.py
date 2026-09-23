#!/usr/bin/env python3
from PIL import Image

head = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise/head_unit/head_xuanji_tortoise_stock_512.png")
print("Head 512 bbox:", head.getbbox(), "size:", head.size)

chassis = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise/chassis/paint_tortoise_jade_512.png")
# collar is around y=180..230, x=200..300
collar_crop = chassis.crop((200, 180, 300, 240))
print("Collar crop bbox:", collar_crop.getbbox())
