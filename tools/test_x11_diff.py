from PIL import Image, ImageChops

im1 = Image.open("proofs/combat_feel/x11_frame_early.png")
im2 = Image.open("proofs/combat_feel/x11_frame_mid.png")
diff = ImageChops.difference(im1, im2)
print("x11 early vs mid diff bbox:", diff.getbbox())
