from PIL import Image

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/attack.png")
# Crop hand and weapon area
crop = im.crop((80, 45, 125, 75))
crop_16x = crop.resize((crop.width * 16, crop.height * 16), Image.Resampling.NEAREST)
crop_16x.save("/tmp/attempt2_hand_16x.png")
print("Saved /tmp/attempt2_hand_16x.png, size:", crop_16x.size)
