from PIL import Image

m_im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit/composite_final_master.png").convert("RGBA")
w, h = m_im.size
data = m_im.load()

print("=== Hand in composite_final_master.png (x: 32..48, y: 72..88) ===")
for y in range(72, 88):
    row = ""
    for x in range(32, 48):
        r, g, b, a = data[x, y]
        if a == 0:
            row += "........"
        else:
            row += f"[{r:02x}{g:02x}{b:02x}]"
    print(f"y={y:2d}: {row}")
