from PIL import Image

im = Image.open('screenshots/proof_battle_macaque_full_screen.png')
# Player is around x=300..450, y=360..540
# Let's crop player feet
feet = im.crop((280, 450, 480, 550))
feet.save('screenshots/test_macaque_feet.png')
print("Saved test_macaque_feet.png")
