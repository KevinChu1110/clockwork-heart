#!/usr/bin/env python3
from PIL import Image

idle_x3 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/macaque_idle_x3.png").convert("RGBA")
ivory = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png").convert("RGBA")

w, h = idle_x3.size
print("Size:", w, h)

# In idle_x3, what are the layers that were composited?
# Let's check the alpha of ivory vs idle_x3
ivory_alpha = [ivory.getpixel((x, y))[3] > 0 for y in range(h) for x in range(w)]
idle_alpha = [idle_x3.getpixel((x, y))[3] > 0 for y in range(h) for x in range(w)]

print("Ivory opaque count:", sum(ivory_alpha))
print("Idle_x3 opaque count:", sum(idle_alpha))

# Let's check overlap:
both = [a and b for a, b in zip(ivory_alpha, idle_alpha)]
print("Both opaque count:", sum(both))
