from PIL import Image

idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/rabbit_idle_x3.png").convert("RGBA")
crop = idle.crop((30, 70, 60, 110))
crop.resize((300, 400), getattr(Image, 'Resampling', Image).NEAREST).save("/tmp/hand_region_idle.png")
print("Saved hand region idle")
