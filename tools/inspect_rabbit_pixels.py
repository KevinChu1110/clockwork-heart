from PIL import Image

im = Image.open("/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_5b8dc14c/proofs/proof_lobby_rimlight_shadow.png")
# 白兔頭頂中心約在 (640, 290~330)
# 檢查 x=640, y 從 250 到 330 的像素
print("--- White rabbit top of head (x=640) ---")
for y in range(250, 320, 5):
    print(f"y={y}: {im.getpixel((640, y))}")

# 檢查耳朵邊緣 x=590~630, y=280
print("--- White rabbit ear edge (y=280) ---")
for x in range(580, 640, 5):
    print(f"x={x}: {im.getpixel((x, 280))}")
