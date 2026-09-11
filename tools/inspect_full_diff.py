from PIL import Image, ImageChops

im1 = Image.open("proofs/combat_feel/rabbit_proof_01_idle.png")
im2 = Image.open("proofs/combat_feel/rabbit_proof_02_attack_lunge.png")
diff = ImageChops.difference(im1, im2)
print("Rabbit proof 1 vs 2 full diff bbox:", diff.getbbox())

im3 = Image.open("proofs/combat_feel/rabbit_proof_03_damage_hit.png")
diff3 = ImageChops.difference(im1, im3)
print("Rabbit proof 1 vs 3 full diff bbox:", diff3.getbbox())

im4 = Image.open("proofs/combat_feel/rabbit_proof_04_break.png")
diff4 = ImageChops.difference(im1, im4)
print("Rabbit proof 1 vs 4 full diff bbox:", diff4.getbbox())
