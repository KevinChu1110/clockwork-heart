from PIL import Image, ImageChops

im20 = Image.open("proofs/combat_feel/tmp_rf/frame_020.png")
im40 = Image.open("proofs/combat_feel/tmp_rf/frame_040.png")
im80 = Image.open("proofs/combat_feel/tmp_rf/frame_080.png")

# 比對角色區域
c20 = im20.crop((180, 180, 500, 480))
c40 = im40.crop((180, 180, 500, 480))
c80 = im80.crop((180, 180, 500, 480))

print("20 vs 40 char diff:", ImageChops.difference(c20, c40).getbbox())
print("20 vs 80 char diff:", ImageChops.difference(c20, c80).getbbox())
