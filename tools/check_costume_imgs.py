from PIL import Image

tunic = Image.open("game/assets/sprites/player/paperdoll/macaque/costume/costume_dawn_monk_tunic.png").convert("RGBA")
zen = Image.open("game/assets/sprites/player/paperdoll/macaque/costume/costume_zen_striker.png").convert("RGBA")

print("Tunic size:", tunic.size, "bbox:", tunic.getbbox())
print("Zen size:", zen.size, "bbox:", zen.getbbox())
