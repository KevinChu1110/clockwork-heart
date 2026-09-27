from PIL import Image
import numpy as np

p = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/owl/back_curio/curio_owl_floating_micro_orrery.png"
im = Image.open(p).convert("RGBA")
arr = np.array(im)
for y in range(45, 75, 3):
    row = [f"({arr[y,x,0]},{arr[y,x,1]},{arr[y,x,2]},{arr[y,x,3]})" for x in range(95, 120, 5)]
    print(f"y={y}:", " ".join(row))
