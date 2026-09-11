from PIL import Image

im = Image.open("/tmp/old_blade.png")
print("Old blade bbox:", im.getbbox())
im.resize((512, 512), getattr(Image, 'Resampling', Image).NEAREST).save("/tmp/old_blade_4x.png")
