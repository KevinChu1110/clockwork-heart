from PIL import Image

im = Image.open("/opt/side/bravesoul-game/screenshots/proof_wardrobe_dialog.png")
# Crop stage panel: x around 285..535, y around 173..533
stage_crop = im.crop((280, 160, 550, 540))
stage_crop.save("/tmp/stage_actual_screenshot.png")

# Also crop the preview rect specifically
prev_crop = im.crop((300, 200, 520, 420))
prev_crop.save("/tmp/preview_actual_screenshot.png")
print("Cropped actual screenshot successfully!")
