from PIL import Image

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/weapon/wpn_spring_claws.png")
# Left hand claws are around x: 18..45, y: 68..103
crop = im.crop((18, 68, 45, 103))
crop_16x = crop.resize((crop.width * 16, crop.height * 16), Image.Resampling.NEAREST)
crop_16x.save("/tmp/idle_claws_approved_16x.png")
print("Saved /tmp/idle_claws_approved_16x.png")
