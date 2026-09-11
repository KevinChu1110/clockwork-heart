from PIL import Image

comp = Image.open("/tmp/test_attack_solid.png")
crop = comp.crop((80, 45, 125, 75))
crop_16x = crop.resize((crop.width * 16, crop.height * 16), Image.Resampling.NEAREST)
crop_16x.save("/tmp/test_hand_solid_16x.png")
print("Saved /tmp/test_hand_solid_16x.png")
