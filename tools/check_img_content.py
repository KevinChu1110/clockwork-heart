from PIL import Image

im = Image.open("proofs/combat_feel/rabbit_proof_01_idle.png")
print("Size:", im.size, "Mode:", im.mode, "Extrema:", im.getextrema())
