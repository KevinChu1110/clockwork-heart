from PIL import Image

im = Image.open("/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_5b8dc14c/proofs/proof_lobby_rimlight_shadow.png")
# 找出所有深色像素 (R<60, G<60, B<60) 在 y=450~650, x=500~780
shadow_pixels = []
for y in range(450, 650):
    for x in range(500, 780):
        r, g, b, a = im.getpixel((x, y))
        if r < 60 and g < 60 and b < 60:
            shadow_pixels.append((x, y, r, g, b))

print(f"Total dark pixels: {len(shadow_pixels)}")
if shadow_pixels:
    ys = [p[1] for p in shadow_pixels]
    xs = [p[0] for p in shadow_pixels]
    print(f"X range: {min(xs)} to {max(xs)}, Y range: {min(ys)} to {max(ys)}")
