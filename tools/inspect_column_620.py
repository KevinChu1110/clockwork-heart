from PIL import Image

im = Image.open("/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_5b8dc14c/proofs/proof_lobby_rimlight_shadow.png")
# 白兔肯定在中間 x=480~800
# 找在 x=620 處從 y=200 到 600 每隔 10px 的像素值
for y in range(200, 600, 10):
    print(f"y={y}: {im.getpixel((620, y))}")
