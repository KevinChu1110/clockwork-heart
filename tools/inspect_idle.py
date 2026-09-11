from PIL import Image

r_idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/rabbit_idle_x3.png").convert("RGBA")
print("rabbit_idle_x3 bbox:", r_idle.getbbox())
r_idle.resize((512, 512), getattr(Image, 'Resampling', Image).NEAREST).save("/tmp/rabbit_idle_x3_4x.png")
