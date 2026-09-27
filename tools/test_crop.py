from PIL import Image

img = Image.open('/opt/side/bravesoul-game/proofs/creation-tabs-i18n/proof_creation_launch_zh_TW.png')
colors = img.crop((650, 630, 1230, 708)).getcolors(maxcolors=10000)
print("Colors in (650, 630, 1230, 708):", colors)

# Let's inspect where BtnConfirm actually is on the screen!
# Let's search the whole image for non-background colors in the bottom half
for y in range(400, 720, 10):
    row_colors = set(img.getpixel((x, y)) for x in range(650, 1230, 10))
    print(f"y={y}: num unique colors = {len(row_colors)}")
