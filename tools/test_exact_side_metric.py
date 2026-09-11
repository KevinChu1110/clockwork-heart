from PIL import Image
import numpy as np

def measure_specks(img_path):
    im = Image.open(img_path).convert("RGBA")
    w, h = im.size
    px = im.load()
    
    # 內部像素＝四鄰都不透明
    inner_count = 0
    dark_count = 0
    
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            # 四鄰都不透明
            if x > 0 and x < w - 1 and y > 0 and y < h - 1:
                if px[x-1, y][3] > 0 and px[x+1, y][3] > 0 and px[x, y-1][3] > 0 and px[x, y+1][3] > 0:
                    inner_count += 1
                    mx = max(r, g, b)
                    if 30 < mx < 110:
                        dark_count += 1
                        
    pct = (dark_count / inner_count * 100) if inner_count > 0 else 0
    return pct, dark_count, inner_count

rab_pct, r_d, r_i = measure_specks("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit/chassis/paint_ivory_stock.png")
iv_pct, iv_d, iv_i = measure_specks("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png")
br_pct, br_d, br_i = measure_specks("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_bamboo_bronze.png")

print(f"Rabbit: {rab_pct:.2f}% ({r_d}/{r_i})")
print(f"Macaque Ivory: {iv_pct:.2f}% ({iv_d}/{iv_i})")
print(f"Macaque Bronze: {br_pct:.2f}% ({br_d}/{br_i})")
