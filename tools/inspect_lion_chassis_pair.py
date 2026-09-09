from PIL import Image

gold = Image.open('game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold.png').convert('RGBA')
ivory = Image.open('game/assets/sprites/player/paperdoll/lion/chassis/paint_ivory_stock.png').convert('RGBA')

print("Gold size:", gold.size, "bbox:", gold.getbbox())
print("Ivory size:", ivory.size, "bbox:", ivory.getbbox())

# Check alpha mask difference between gold and ivory
diff_alpha = 0
for y in range(128):
    for x in range(128):
        if gold.getpixel((x, y))[3] != ivory.getpixel((x, y))[3]:
            diff_alpha += 1
print("Diff in alpha between gold and ivory chassis:", diff_alpha)
