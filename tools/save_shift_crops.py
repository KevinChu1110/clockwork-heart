from PIL import Image

f67 = Image.open("/opt/side/bravesoul-game/proofs/macaque_frames/f_0067.png").convert("RGBA")
f68 = Image.open("/opt/side/bravesoul-game/proofs/macaque_frames/f_0068.png").convert("RGBA")
f78 = Image.open("/opt/side/bravesoul-game/proofs/macaque_frames/f_0078.png").convert("RGBA")

# Crop player slot x in [150, 480], y in [200, 550]
f67.crop((150, 200, 480, 550)).save("/tmp/f67_player.png")
f68.crop((150, 200, 480, 550)).save("/tmp/f68_player.png")
f78.crop((150, 200, 480, 550)).save("/tmp/f78_player.png")
print("Saved /tmp/f67_player.png, /tmp/f68_player.png, /tmp/f78_player.png")
