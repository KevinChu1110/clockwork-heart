from PIL import Image

for i in range(20, 31):
    fn = f"f_{i:04d}.png"
    im = Image.open(f"/opt/side/bravesoul-game/proofs/macaque_frames/{fn}").convert("RGBA")
    crop = im.crop((150, 200, 550, 600))
    crop.save(f"/tmp/frame_{i:02d}_crop.png")

print("Saved frames 20..30 crops")
