from PIL import Image

def measure_im(im, name=""):
    w, h = im.size
    px = im.load()
    def op(x, y):
        return 0 <= x < w and 0 <= y < h and px[x, y][3] >= 128
    n = 0
    tot = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 128: continue
            if not(op(x-1, y) and op(x+1, y) and op(x, y-1) and op(x, y+1)): continue
            tot += 1
            mx = max(r, g, b)
            if 30 < mx < 110: n += 1
    pct = n / max(tot, 1) * 100
    print(f"{name:30s} interior={tot:5d} darkspeckle={n:5d} ({pct:5.2f}%)")
    return n

base = "game/assets/sprites/player/paperdoll/rabbit"
slots = [
    ("winding_key", f"{base}/winding_key/key_classic_brass.png"),
    ("back_curio", f"{base}/back_curio/curio_steam_exhaust.png"),
    ("chassis", f"{base}/chassis/paint_ivory_stock.png"),
    ("head_unit", f"{base}/head_unit/ear_rabbit_straight.png"),
    ("costume", f"{base}/costume/costume_nutcracker_guard.png"),
    ("optic_core", f"{base}/optic_core/core_cyan_emerald.png"),
    ("weapon", f"{base}/weapon/wpn_dawn_blade.png")
]

comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
for sname, spath in slots:
    layer = Image.open(spath).convert("RGBA")
    comp.alpha_composite(layer)
    measure_im(comp, f"Rabbit + {sname}")
