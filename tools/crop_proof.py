from PIL import Image
im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/proof_paperdoll_macaque_composite.png")
c = im.crop((40, 25, 85, 65))
c.save("/opt/side/bravesoul-game/screenshots/proof_composite_face.png")
print("Saved proof_composite_face.png")
