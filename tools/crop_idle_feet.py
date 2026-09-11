from PIL import Image

im = Image.open("screenshots/proof_battle_equipped_royal_parade.png")
crop = im.crop((300, 420, 660, 600))
crop.save("screenshots/test_idle_feet_crop.png")
print("Saved test_idle_feet_crop.png size:", crop.size)
