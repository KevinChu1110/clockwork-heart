from PIL import Image

r_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit"
navy = Image.open(f"{r_dir}/chassis/paint_midnight_navy.png").convert("RGBA")
ivory = Image.open(f"{r_dir}/chassis/paint_ivory_stock.png").convert("RGBA")

# Let's crop x: 30..48, y: 72..90
navy.crop((30, 72, 48, 90)).resize((180, 180), getattr(Image, 'Resampling', Image).NEAREST).save("/tmp/chassis_hand_navy.png")
ivory.crop((30, 72, 48, 90)).resize((180, 180), getattr(Image, 'Resampling', Image).NEAREST).save("/tmp/chassis_hand_ivory.png")
print("Saved chassis hand crops")
