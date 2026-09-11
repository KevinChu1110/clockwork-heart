from PIL import Image

im_dawn = Image.open("/opt/side/bravesoul-game/screenshots/proof_battle_macaque_equipped_dawn_monk.png").convert("RGBA")
print("dawn size:", im_dawn.size)
c = im_dawn.crop((200, 180, 580, 660))
c.save("/tmp/test_crop_dawn.png")
print("saved /tmp/test_crop_dawn.png")
