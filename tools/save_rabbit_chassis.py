from PIL import Image
r_chassis = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit/chassis/paint_ivory_stock.png")
print("rabbit chassis size:", r_chassis.size)
r_chassis.save("/opt/side/bravesoul-game/screenshots/rabbit_chassis.png")
