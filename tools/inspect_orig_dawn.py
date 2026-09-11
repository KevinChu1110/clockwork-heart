from PIL import Image

im = Image.open("/tmp/original_dawn_blade.png")
print("Original dawn blade bbox:", im.getbbox())
im.resize((512, 512), getattr(Image, 'Resampling', Image).NEAREST).save("/tmp/original_dawn_blade_4x.png")
