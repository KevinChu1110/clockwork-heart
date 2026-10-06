from PIL import Image

im = Image.open("game/assets/sprites/player/showcase/rabbit_idle_hd.png")
print("size:", im.size, "bbox:", im.getbbox())
