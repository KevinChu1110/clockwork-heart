import os
from PIL import Image
import numpy as np

repo = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_e4a76321"
idle_path = f"{repo}/game/assets/sprites/player/poses/firefly/idle.png"
im = Image.open(idle_path)
arr = np.array(im)

print("Shape:", arr.shape)
counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print("Shadow rows 118..127 counts:", counts)
expected_marmot = [59, 57, 53, 45, 29, 0, 0, 0, 0, 0]
print("Matches standard expected shadow:", counts == expected_marmot)
