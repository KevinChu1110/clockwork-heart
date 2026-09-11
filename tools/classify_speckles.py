from PIL import Image
import numpy as np

im = Image.open('game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png').convert('RGBA')
w, h = im.size
px = im.load()

def op(x, y):
    return 0 <= x < w and 0 <= y < h and px[x, y][3] >= 128

# Identify dark speckles
speckles = []
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        if a < 128: continue
        if not (op(x-1,y) and op(x+1,y) and op(x,y-1) and op(x,y+1)): continue
        mx = max(r, g, b)
        if 30 < mx < 110:
            speckles.append((x, y, (r, g, b)))

print(f"Total dark speckles: {len(speckles)}")

# Criteria for PRESERVED structural elements:
# 1. Eyes:
# Left eye: x=46..54, y=42..50
# Right eye: x=66..76, y=42..51
# 2. Nose nostril dots: x=52..56, y=54..57
# 3. Mouth line: x=50..64, y=59..62 (only the main horizontal smile line, 1px)
# 4. Neck mechanical axis: center x=45..55, y=66..72 (cylindrical hinge)
# 5. Boots/legs: y >= 105
# 6. Hand knuckles/wrists: natural joint lines
def is_structural(x, y):
    # Boots & legs
    if y >= 105:
        return True
        
    # Eyes sensor and crisp frame
    if 45 <= x <= 55 and 41 <= y <= 51:
        # Check if it is eye pupil or immediate eye contour
        return True
    if 66 <= x <= 75 and 41 <= y <= 50:
        return True
        
    # Nostrils
    if 51 <= x <= 57 and 54 <= y <= 57:
        return True
        
    # Smile line (1px clean smile)
    if 48 <= x <= 62 and 59 <= y <= 62:
        # We will refine smile line so it's a single clean line
        # If it's part of the horizontal smile line
        if y == 60 or (y == 59 and (x <= 50 or x >= 60)):
            return True

    # Neck joint center cylinder (x=45..53, y=66..70)
    if 44 <= x <= 53 and 66 <= y <= 71:
        return True
        
    # Left ear hinge (x=33..36, y=36..40) - only the hinge pivot
    # Right ear hinge (x=83..86, y=39..42)
    
    return False

structural = [s for s in speckles if is_structural(s[0], s[1])]
dirt = [s for s in speckles if not is_structural(s[0], s[1])]

print(f"Structural (preserved): {len(structural)}")
print(f"Dirt / cracks (to be cleaned): {len(dirt)}")
print(f"If cleaned, remaining speckles: {len(structural)} / 4321 = {len(structural)/4321*100:.2f}%")
