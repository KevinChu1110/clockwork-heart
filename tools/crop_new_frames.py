from PIL import Image

f78 = Image.open("/opt/side/bravesoul-game/proofs/macaque_frames/f_0078.png").convert("RGBA")
# Crop player at f78
crop78 = f78.crop((180, 220, 500, 520))
crop78.save("/tmp/new_p_f78.png")

# Also crop player at f23
f23 = Image.open("/opt/side/bravesoul-game/proofs/macaque_frames/f_0023.png").convert("RGBA")
crop23 = f23.crop((180, 220, 500, 520))
crop23.save("/tmp/new_p_f23.png")

print("Saved /tmp/new_p_f78.png and /tmp/new_p_f23.png")
