from PIL import Image

fs = Image.open("screenshots/proof_battle_macaque_full_screen.png").convert("RGBA")
crop = fs.crop((220, 220, 460, 600))
crop.save("/tmp/fs_macaque_crop.png")
print("Saved /tmp/fs_macaque_crop.png")
