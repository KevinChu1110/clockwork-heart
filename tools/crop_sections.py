from PIL import Image

idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png").convert("RGBA")

# Let's crop 4 quadrants or sections:
# Upper: head
# Left: left arm / weapon?
# Right: right arm / weapon?
# Center: body

c_left = idle.crop((20, 60, 60, 120))
c_left.resize((160, 240), getattr(Image, 'Resampling', Image).NEAREST).save("/tmp/idle_left.png")

c_right = idle.crop((60, 60, 100, 120))
c_right.resize((160, 240), getattr(Image, 'Resampling', Image).NEAREST).save("/tmp/idle_right.png")

c_center = idle.crop((40, 60, 80, 120))
c_center.resize((160, 240), getattr(Image, 'Resampling', Image).NEAREST).save("/tmp/idle_center.png")

print("Saved /tmp/idle_left.png, idle_right.png, idle_center.png")
