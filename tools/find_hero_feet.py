from PIL import Image

im = Image.open("/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_5b8dc14c/proofs/proof_lobby_rimlight_shadow.png")
# 檢查 x=550~730, y=450~630 區域
# 看看角色白色像素在哪裡結束（腳底）
feet_y = 0
for y in range(400, 600):
    for x in range(600, 680):
        p = im.getpixel((x, y))
        # 白兔靴子或褲子大多是較高亮度的白色或深靴子
        # 看看何時離開角色
        pass

# 檢查 stage_anchor 下各個節點在圖上的位置：
# stage_anchor 位於 (640, 360 + 45) = (640, 405)
# _hero_avatar 在 offset_top = -150, offset_bottom = 170 (y = 255 到 575)
# _hero_shadow 在 offset_top = 74, offset_bottom = 120 (y = 479 到 525)
print("Hero avatar global Y range: 255 to 575")
print("Hero shadow global Y range: 479 to 525")
# 為什麼 shadow 在 479~525？如果 hero avatar 底部是 575，那 479~525 正好在角色膝蓋或腰部後面！
