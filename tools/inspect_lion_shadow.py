from PIL import Image

gold = Image.open('game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold.png').convert('RGBA')
print("Checking lion ground shadow in gold:")
shadow_pts = 0
total_pts = 0
for y in range(118, 124):
    for x in range(36, 93):
        total_pts += 1
        p = gold.getpixel((x, y))
        if p[3] >= 60:
            shadow_pts += 1
print(f"Shadow points: {shadow_pts}/{total_pts} = {shadow_pts/total_pts*100:.1f}%")
print("Sample shadow pixels at Y=120:")
for x in range(45, 60, 3):
    print(f"  X={x}: {gold.getpixel((x, 120))}")
