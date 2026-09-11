from PIL import Image

im = Image.open("screenshots/proof_battle_lion_full_screen.png")
# Crop left side at y=350..420, x=0..260
crop = im.crop((0, 350, 260, 420))
crop.save("/tmp/left_y384.png")
print("Saved /tmp/left_y384.png")
