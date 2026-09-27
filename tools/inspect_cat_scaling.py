from PIL import Image

p = "game/assets/sprites/player/showcase/cat_idle_hd.png"
img = Image.open(p)
print("Cat bbox:", img.getbbox())
p512 = "game/assets/sprites/player/paperdoll/cat"
# Let's inspect cat build script
