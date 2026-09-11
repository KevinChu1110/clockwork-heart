from PIL import Image

im = Image.open("screenshots/proof_battle_lion_full_screen.png")
# Crop player at full screen: around x=260..420, y=280..520
crop = im.crop((260, 280, 420, 520))
crop.save("/tmp/lion_fullscreen_player.png")
print("Saved /tmp/lion_fullscreen_player.png")
