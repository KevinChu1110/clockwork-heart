from PIL import Image

im = Image.open("screenshots/proof_battle_attack_sword.png")
crop = im.crop((300, 420, 660, 600))
crop.save("screenshots/test_attack_feet_crop.png")
print("Saved test_attack_feet_crop.png size:", crop.size)
