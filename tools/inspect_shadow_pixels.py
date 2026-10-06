from PIL import Image

im = Image.open("/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_5b8dc14c/proofs/proof_lobby_rimlight_shadow.png")
# 檢查展台與陰影區域 (x=640, y=530~600)
# stage_anchor y=405, pedestal y=155 -> global y = 560
print("--- Stage Pedestal & Shadow Pixels (x=640) ---")
for y in range(530, 600, 5):
    print(f"y={y}: {im.getpixel((640, y))}")

print("--- Foot Shadow across X (y=560) ---")
for x in range(580, 710, 10):
    print(f"x={x}: {im.getpixel((x, 560))}")
