from PIL import Image

im = Image.open("/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_5b8dc14c/proofs/proof_lobby_rimlight_shadow.png")
print("Size:", im.size)
for y in range(400, 700, 15):
    print(f"y={y}: {im.getpixel((640, y))}")
