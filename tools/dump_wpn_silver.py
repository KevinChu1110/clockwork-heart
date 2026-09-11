from PIL import Image

wpn = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit/weapon/wpn_dawn_blade.png").convert("RGBA")
w, h = wpn.size
silver_pts = []
for y in range(h):
    for x in range(w):
        r, g, b, a = wpn.getpixel((x, y))
        if a > 128 and r > 195 and g > 195 and b > 195 and abs(r - b) < 40:
            silver_pts.append((x, y, r, g, b))

print("wpn_dawn_blade.png silver pixels count:", len(silver_pts))
for p in silver_pts:
    print(f"({p[0]}, {p[1]}): RGB({p[2]}, {p[3]}, {p[4]})")
