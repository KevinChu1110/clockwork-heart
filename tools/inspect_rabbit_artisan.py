from PIL import Image

r_art = Image.open('game/assets/sprites/player/paperdoll/rabbit/costume/costume_steam_artisan.png')
w, h = r_art.size
pts = []
colors = {}
for y in range(h):
    for x in range(w):
        p = r_art.getpixel((x, y))
        if p[3] > 20:
            pts.append((x, y))
            colors[p[:3]] = colors.get(p[:3], 0) + 1

print("Rabbit steam artisan points:", len(pts))
print(f"X: {min(p[0] for p in pts)}..{max(p[0] for p in pts)}, Y: {min(p[1] for p in pts)}..{max(p[1] for p in pts)}")
print("Top 15 colors:")
for c, cnt in sorted(colors.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f"  RGB {c}: {cnt}")
