from PIL import Image

for f in ["f_0077.png", "f_0078.png", "f_0079.png", "f_0080.png", "f_0081.png", "f_0082.png"]:
    im = Image.open(f"/opt/side/bravesoul-game/proofs/macaque_frames/{f}").convert("RGBA")
    # Crop player
    crop = im.crop((180, 250, 480, 520))
    crop.save(f"/tmp/p_{f}")

print("Saved p_f_0077..82")
