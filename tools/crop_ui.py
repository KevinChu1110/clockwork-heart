from PIL import Image

im = Image.open("screenshots/proof_battle_lion_full_screen.png")
crop = im.crop((80, 370, 200, 400))
crop.save("/tmp/ui_box.png")
print("Saved /tmp/ui_box.png")
