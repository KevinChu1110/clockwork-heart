from PIL import Image
orig = Image.open("/opt/side/bravesoul-game/screenshots/chassis_orig.png")
c = orig.crop((40, 25, 85, 65))
c.save("/opt/side/bravesoul-game/screenshots/chassis_orig_face.png")
print("Saved chassis_orig_face.png")
