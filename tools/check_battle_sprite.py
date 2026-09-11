import sys
sys.path.insert(0, '/opt/side/bravesoul-game')
from tools.measure_speckle import interior_speckle

print("Macaque battle:")
interior_speckle("game/assets/sprites/player/macaque_battle.png")
print("Rabbit battle:")
interior_speckle("game/assets/sprites/player/rabbit_battle.png")
