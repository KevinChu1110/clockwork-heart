from PIL import Image

trans = Image.open("/tmp/char_rabbit_trans.png")
dark_bg = Image.new("RGBA", trans.size, (7, 7, 9, 255))
dark_bg.paste(trans, (0, 0), trans)
dark_bg.save("/tmp/char_rabbit_on_dark.png")
print("Saved /tmp/char_rabbit_on_dark.png")
