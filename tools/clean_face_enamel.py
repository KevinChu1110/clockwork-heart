#!/usr/bin/env python3
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png").convert("RGBA")
w, h = im.size

# Let's clean the face (y: 18..54, x: 32..86)
# First, let's identify the mouth seam:
# In macaque, mouth is around y=48..50, x=48..54
# Eye sockets: left eye around y=38..43, x=39..44; right eye around y=38..43, x=62..66.
#
# Any other dark pixel (val < 140) inside the face area (y: 18..54, x: 32..86)
# is noise/crack/speck!
# Let's clean them:
cleaned = im.copy()

for y in range(18, 54):
    for x in range(32, 86):
        r, g, b, a = im.getpixel((x, y))
        if a < 200:
            continue
        val = (r + g + b) // 3
        # Check if it's the shape outline:
        # A pixel is an outer outline if it has adjacent transparent pixels
        is_outer_border = False
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if im.getpixel((x + dx, y + dy))[3] < 100:
                    is_outer_border = True
                    break
            if is_outer_border:
                break
        if is_outer_border:
            continue
        
        # If it's a dark pixel (val < 140):
        # Is it part of the eye socket or mouth?
        # Mouth seam: y in (48, 49), x in (48..53) -> keep
        if y in (48, 49) and 48 <= x <= 53:
            continue
        # Left eye socket: y in (39..43), x in (40..44) -> keep
        if 39 <= y <= 43 and 40 <= x <= 44:
            continue
        # Right eye socket / inner corner: y in (39..43), x in (63..65) -> keep
        if 39 <= y <= 43 and 63 <= x <= 65:
            continue

        if val < 150:
            # It is a crack, speck, or dither noise!
            # Find light neighbors (val > 180) in a 7x7 window
            light_nbrs = []
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h:
                        nr, ng, nb, na = im.getpixel((nx, ny))
                        if na > 200 and ((nr + ng + nb) // 3) > 175:
                            light_nbrs.append((nr, ng, nb))
            if light_nbrs:
                ar = sum(c[0] for c in light_nbrs) // len(light_nbrs)
                ag = sum(c[1] for c in light_nbrs) // len(light_nbrs)
                ab = sum(c[2] for c in light_nbrs) // len(light_nbrs)
                cleaned.putpixel((x, y), (ar, ag, ab, 255))

cleaned.crop((35, 20, 95, 60)).save("/tmp/test_clean_face_v2.png")
print("Saved /tmp/test_clean_face_v2.png")
