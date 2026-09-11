from PIL import Image

im = Image.open("proofs/combat_feel/tmp_10s/frame_271.png")
c = im.crop((700, 80, 1150, 420))
c.save("proofs/combat_feel/frame_271_enemy.png")
print("Saved frame_271_enemy.png")
