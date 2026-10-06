from PIL import Image

im = Image.open("/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_5b8dc14c/proofs/proof_lobby_rimlight_shadow.png")
# 白兔身體在 x=600~680 區間，找所有白色/非背景像素的 y 範圍
# 背景色約在 (220~250, 190~230, 130~190)
hero_pixels = []
for y in range(200, 650):
    for x in range(600, 680):
        r, g, b, a = im.getpixel((x, y))
        # 白兔靴子是深褐/黑金屬色，衣服是深藍/紅，臉是純白
        # 看看何時進入和離開主角
        # 純白臉/手: r>250, g>250, b>250
        # 胡桃鉗紅衣: r>180, g<80, b<80
        # 深色靴子: r<100, g<80, b<80
        if (r > 245 and g > 245 and b > 245) or (r > 160 and g < 70 and b < 70) or (r < 60 and g < 50 and b < 50):
            hero_pixels.append((x, y, r, g, b))

print(f"Total hero pixels detected: {len(hero_pixels)}")
if hero_pixels:
    ys = [p[1] for p in hero_pixels]
    print(f"Hero Y top: {min(ys)}, Hero Y bottom (feet): {max(ys)}")
