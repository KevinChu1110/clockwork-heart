from PIL import Image
import numpy as np

img = Image.open("/opt/side/bravesoul-game/screenshots/qa_round2/proof_07_battle_macaque.png")
print("Image size:", img.size)

# Find coordinates where white/near-white or semi-transparent rectangle is on the left side
# Let's crop x: 50..350, y: 100..400
crop = img.crop((50, 80, 400, 450))
crop.save("/opt/side/bravesoul-game/screenshots/qa_round2/crop_macaque.png")
print("Saved crop_macaque.png")

arr = np.array(crop)
print("Crop shape:", arr.shape)
