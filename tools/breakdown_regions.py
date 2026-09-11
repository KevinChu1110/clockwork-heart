from PIL import Image

im = Image.open('game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png').convert('RGBA')
w, h = im.size
px = im.load()

def op(x, y):
    return 0 <= x < w and 0 <= y < h and px[x, y][3] >= 128

regions = {
    "1_forehead_crown (y<45)": lambda x, y: y < 45,
    "2_face_cheeks (45<=y<65)": lambda x, y: 45 <= y < 65,
    "3_neck_shoulders (65<=y<78)": lambda x, y: 65 <= y < 78,
    "4_torso_belly (78<=y<105, 38<=x<=78)": lambda x, y: 78 <= y < 105 and 38 <= x <= 78,
    "5_arms_hands (78<=y<115, x<38 or x>78)": lambda x, y: 78 <= y < 115 and (x < 38 or x > 78),
    "6_crotch_legs (y>=105)": lambda x, y: y >= 105
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

print("--- Regional Breakdown of Macaque Ivory Chassis ---")
for name in regions:
    c = counts[name]
    tot = inners[name]
    pct = c / max(tot, 1) * 100
    print(f"{name:40s}: {c:4d} / {tot:4d} ({pct:5.2f}%)")
