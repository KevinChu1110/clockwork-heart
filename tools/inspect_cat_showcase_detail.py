from PIL import Image

p = "game/assets/sprites/player/showcase/cat_idle_hd.png"
img = Image.open(p)
print("Cat showcase size:", img.size, "bbox:", img.getbbox())
# Cat width in showcase was 783, margin L=8, R=9!
# Because for cat, char_crop_512 width was smaller, so sc_w was ~783!
