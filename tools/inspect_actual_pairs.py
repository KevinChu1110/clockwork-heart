from PIL import Image

idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png").convert("RGBA")
screen = Image.open("/opt/side/bravesoul-game/proofs/combat_feel/rabbit_battle_idle.png").convert("RGB")

scale = 200.0 / 128.0
ox = 224.0
oy = 248.0

print("Sampling blade pixels in idle.png and corresponding screen pixels:")
# In idle.png, let's look at y in [75, 95], x in [60, 80]
for y in [78, 82, 86, 90, 93]:
    for x in [64, 68, 72, 76]:
        ip = idle.getpixel((x, y))
        sx = int(ox + (x + 0.5) * scale)
        sy = int(oy + (y + 0.5) * scale)
        sp = screen.getpixel((sx, sy))
        print(f"idle({x:2d}, {y:2d})={ip[:3]} (r-b={ip[0]-ip[2]}) --> screen({sx}, {sy})={sp} (r-b={sp[0]-sp[2]})")
