#!/usr/bin/env python3
from PIL import Image
import numpy as np

body = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/maple_parts/body/paint_brass_gold.png").convert("RGBA")
arr = np.array(body)

# Let's check what is in body at x: 300..450, y: 60..180
crop = body.crop((300, 60, 450, 180))
crop.save("/tmp/body_key_area.png")

# Also check head at the ear area
head = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl_brass.png").convert("RGBA")
head.save("/tmp/head_brass.png")

print("Saved /tmp/body_key_area.png and /tmp/head_brass.png")
