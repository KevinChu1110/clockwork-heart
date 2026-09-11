from PIL import Image

im = Image.open('/opt/side/bravesoul-game/proofs/hud_dopamine/proof_explore_hud_hotbar.png')
# Let's inspect pixels around:
# 1. Top hint bar "點一下 · 銹蝕長劍" (approx around x=640, y=20)
# 2. "銹蝕長劍" (around x=610, y=490)
# 3. "舊鑰" (around x=750, y=510)
# 4. "玩具堆邊緣" (around x=140, y=410)
# 5. "往天窗" (around x=860, y=430)
# 6. "往玩具堆外緣" (around x=870, y=470)
# 7. "箱底洞穴" (around x=1020, y=140)
# 8. "靜止玩具墓" (around x=1180, y=560)

# Let's search for the cream background pixels #FFFDF8 -> (255, 253, 248) or similar
# and border #1F1A3A -> (31, 26, 58)

# Find bounding boxes of near-cream regions in the image
width, height = im.size
rgb = im.convert('RGB')

print("Sampling specific areas:")
for name, (x, y) in [
    ("Top hint", (640, 24)),
    ("Sword label", (612, 492)),
    ("Oldkey label", (745, 524)),
]:
    colors = [rgb.getpixel((x + dx, y + dy)) for dx in range(-5, 6) for dy in range(-2, 3)]
    # count how many are cream-like (R>245, G>240, B>235) and text-like (R<50, G<45, B<70)
    cream = sum(1 for r,g,b in colors if r > 240 and g > 235 and b > 230)
    dark = sum(1 for r,g,b in colors if r < 60 and g < 50 and b < 80)
    print(f"{name} at ({x}, {y}): sample has {cream} cream pixels, {dark} dark text/border pixels. Center pixel={rgb.getpixel((x,y))}")
