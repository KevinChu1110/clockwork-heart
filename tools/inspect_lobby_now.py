from PIL import Image

p = "proofs/exploratory_qa_t_e6bc1e6c/proof_lobby_hedgehog.png"
img = Image.open(p)
# crop around x=400..900, y=100..600
c = img.crop((460, 180, 860, 580))
c.save("proofs/test_lobby_crop_now.png")
print("Saved test_lobby_crop_now.png")
