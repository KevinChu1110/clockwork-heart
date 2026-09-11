from PIL import Image

idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/rabbit_idle_x3.png").convert("RGBA")
# Where is the sword in rabbit_idle_x3?
# Let's crop the sword from rabbit_idle_x3!
sword_crop = idle.crop((34, 70, 90, 125))
sword_crop.resize((280, 275), getattr(Image, 'Resampling', Image).NEAREST).save("/tmp/idle_sword_crop.png")
print("Saved idle sword crop")
