from PIL import Image

im = Image.open("/opt/side/bravesoul-game/screenshots/proof_wardrobe_dialog.png")
# Crop stage panel: x around 285..535, y around 173..533
stage_crop = im.crop((280, 160, 550, 540))
stage_crop.save("/tmp/stage_final_verified.png")

# Crop preview rect specifically
prev_crop = im.crop((295, 195, 525, 425))
prev_crop.save("/tmp/preview_final_verified.png")
print("Cropped final verified screenshot!")
