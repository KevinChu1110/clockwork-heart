import numpy as np
from PIL import Image

mane = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/head_unit/ear_lion_gilded_mane_512.png')
body = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold_512.png')
core = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/optic_core/core_amber_sun_512.png')

m_arr = np.array(mane)
b_arr = np.array(body)
c_arr = np.array(core)

print("Checking mane eye area (x=186..202, y=162..184):")
m_left_eye = m_arr[162:185, 186:202]
print("Mane left eye alpha min/max:", m_left_eye[:, :, 3].min(), m_left_eye[:, :, 3].max())
print("Mane left eye RGB min/max:", m_left_eye[:, :, :3].min(), m_left_eye[:, :, :3].max())

print("Checking body eye area (x=186..202, y=162..184):")
b_left_eye = b_arr[162:185, 186:202]
print("Body left eye alpha min/max:", b_left_eye[:, :, 3].min(), b_left_eye[:, :, 3].max())

print("Checking core eye area (x=186..202, y=162..184):")
c_left_eye = c_arr[162:185, 186:202]
print("Core left eye alpha min/max:", c_left_eye[:, :, 3].min(), c_left_eye[:, :, 3].max())
print("Core left eye RGB where alpha > 0:")
for y in range(c_left_eye.shape[0]):
    for x in range(c_left_eye.shape[1]):
        if c_left_eye[y, x, 3] > 0:
            print(f"  ({x}, {y}): RGBA={c_left_eye[y, x]}")
            break
