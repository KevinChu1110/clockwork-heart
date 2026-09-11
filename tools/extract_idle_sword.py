from PIL import Image, ImageChops

idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/rabbit_idle_x3.png").convert("RGBA")
ch_ivory = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit/chassis/paint_ivory_stock.png").convert("RGBA")

diff = ImageChops.difference(idle, ch_ivory)
print("Diff bbox between idle and chassis ivory:", diff.getbbox())

# Let's extract the isolated sword from idle where chassis was painted over
# Or let's see what was in idle that is NOT in chassis!
idle_data = idle.load()
ch_data = ch_ivory.load()
w, h = idle.size

isolated_sword = Image.new("RGBA", (w, h), (0, 0, 0, 0))
iso_data = isolated_sword.load()

for y in range(h):
    for x in range(w):
        ip = idle_data[x, y]
        cp = ch_data[x, y]
        if ip[3] > 0 and (ip != cp):
            iso_data[x, y] = ip

print("Isolated sword bbox:", isolated_sword.getbbox())
isolated_sword.save("/tmp/isolated_sword_from_idle.png")
isolated_sword.resize((512, 512), getattr(Image, 'Resampling', Image).NEAREST).save("/tmp/isolated_sword_4x.png")
