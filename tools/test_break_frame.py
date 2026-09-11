from PIL import Image

img = Image.open("/opt/side/bravesoul-game/proofs/combat_feel/macaque_real_04_break.png")
# Crop around enemy region: x: 700..1200, y: 150..550
crop = img.crop((700, 150, 1200, 550))
crop.save("/tmp/enemy_crop_break.png")
print("Saved /tmp/enemy_crop_break.png")
