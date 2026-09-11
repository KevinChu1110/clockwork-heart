import os
from PIL import Image, ImageDraw

atk_orig = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/attack.png").convert("RGBA")
w, h = atk_orig.size

# Let's inspect the original attack sprite bbox
print("Original attack bbox:", atk_orig.getbbox())

# Let's see: In original attack, what is the rightmost x?
# It was 101/102.
# If we add 3 curved claws extending from x=96..100 to x=118..122,
# let's calculate the silhouette visibility ratio and external ratio!
