from PIL import Image

frame_dir = "/opt/side/bravesoul-game/proofs/macaque_frames"

for fn in ["f_0023.png", "f_0024.png", "f_0025.png", "f_0028.png", "f_0078.png", "f_0079.png", "f_0080.png", "f_0081.png"]:
    im = Image.open(f"{frame_dir}/{fn}").convert("RGBA")
    # Crop around player
    crop = im.crop((150, 200, 550, 600))
    crop.save(f"/tmp/player_{fn}")
    print(f"Saved /tmp/player_{fn}")
