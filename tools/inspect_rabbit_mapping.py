#!/usr/bin/env python3
from PIL import Image

gold = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit/chassis/paint_brass_gold.png")
ivory = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit/chassis/paint_ivory_stock.png")
navy = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit/chassis/paint_midnight_navy.png")

# Compare ivory vs gold on rabbit
print("Rabbit ivory vs gold:")
for p in [(60, 60), (64, 80), (55, 90), (70, 70)]:
    print(f"  at {p}: ivory={ivory.getpixel(p)} -> gold={gold.getpixel(p)} -> navy={navy.getpixel(p)}")
