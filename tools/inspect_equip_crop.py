from PIL import Image

im = Image.open("/opt/side/bravesoul-game/final_sky_lobby_verified.png")
w, h = im.size
print(f"Image size: {w}x{h}")

# Crop the top-right area (x: 900 to 1280, y: 0 to 400)
crop = im.crop((950, 0, 1280, 400))
crop.save("/opt/side/bravesoul-game/tools/equip_schematic_crop.png")
print("Saved equip_schematic_crop.png")
