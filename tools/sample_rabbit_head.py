from PIL import Image

rab = Image.open('game/assets/sprites/player/paperdoll/rabbit/chassis/paint_ivory_stock.png').convert('RGBA')
px = rab.load()

print("Sample rabbit head rows:")
for y in [45, 50, 55, 60]:
    row_colors = [px[x, y][:3] for x in range(50, 75) if px[x, y][3] >= 128]
    print(f"y={y}: len={len(row_colors)}, min={min(row_colors)}, max={max(row_colors)}")
