from PIL import Image

r_art = Image.open('game/assets/sprites/player/paperdoll/rabbit/costume/costume_steam_artisan.png').convert('RGBA')
w, h = r_art.size
for y in range(75, 111, 3):
    row = ""
    for x in range(45, 85):
        p = r_art.getpixel((x, y))
        if p[3] == 0:
            row += " "
        elif p[:3] == (31, 26, 58) or p[:3] == (30, 24, 45):
            row += "|"
        elif p[0] > 100 and p[1] > 70 and p[2] < 70:
            row += "*" # brass/bronze
        else:
            row += "#" # body
    print(f"Y={y:3d}: {row}")
