from PIL import Image

im = Image.open('game/assets/sprites/player/paperdoll/rabbit/chassis/paint_ivory_stock.png').convert('RGBA')
w, h = im.size
px = im.load()

def op(x, y):
    return 0 <= x < w and 0 <= y < h and px[x, y][3] >= 128

regions = {
    "1_ears_forehead (y<50)": lambda x, y: y < 50,
    "2_face_cheeks (50<=y<65)": lambda x, y: 50 <= y < 65,
    "3_neck_chest (65<=y<85)": lambda x, y: 65 <= y < 85,
    "4_torso_belly (85<=y<105)": lambda x, y: 85 <= y < 105,
    "5_legs_feet (y>=105)": lambda x, y: y >= 105
}

counts = {k: 0 for k in regions}
inners = {k: 0 for k in regions}

for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        if a < 128: continue
        if not(op(x-1,y) and op(x+1,y) and op(x,y-1) and op(x,y+1)): continue
        
        mx = max(r, g, b)
        is_dark = (30 < mx < 110)
        
        for name, fn in regions.items():
            if fn(x, y):
                inners[name] += 1
                if is_dark:
                    counts[name] += 1

print("--- Regional Breakdown of Rabbit Ivory Chassis ---")
for name in regions:
    c = counts[name]
    tot = inners[name]
    pct = c / max(tot, 1) * 100
    print(f"{name:40s}: {c:4d} / {tot:4d} ({pct:5.2f}%)")
