from PIL import Image

im = Image.open("/tmp/fox_test/char_no_shadow_no_wep.png")
print("char_no_shadow_no_wep size:", im.size, "bbox:", im.getbbox())
