from PIL import Image

im = Image.open('/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit/winding_key/key_classic_brass.png')
print("128x128 size:", im.size, "bbox:", im.getbbox())
