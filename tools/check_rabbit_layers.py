#!/usr/bin/env python3
from PIL import Image

rab_chassis = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit/chassis/paint_ivory_stock.png").convert("RGBA")
rab_ear = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit/head_unit/ear_rabbit_straight.png").convert("RGBA")
rab_core = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit/optic_core/core_cyan_emerald.png").convert("RGBA")

print("Rabbit chassis bbox:", rab_chassis.getbbox())
print("Rabbit ear bbox:    ", rab_ear.getbbox())
print("Rabbit core bbox:   ", rab_core.getbbox())
