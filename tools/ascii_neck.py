from PIL import Image

im = Image.open('game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png').convert('RGBA')
px = im.load()
w, h = im.size

def op(x, y):
    return 0 <= x < w and 0 <= y < h and px[x, y][3] >= 128

print("=== MACAQUE NECK / SHOULDERS (65<=y<78) DARKSPECKLE PIXELS ===")
for y in range(65, 78):
    line = []
    for x in range(25, 95):
        r, g, b, a = px[x, y]
        if a < 128:
            line.append(" ")
        elif not(op(x-1,y) and op(x+1,y) and op(x,y-1) and op(x,y+1)):
            line.append("#") # outline
        else:
            mx = max(r, g, b)
            if 30 < mx < 110:
                line.append("*") # dark speckle
            else:
                line.append(".") # clean surface
    print(f"y={y:2d} " + "".join(line))
