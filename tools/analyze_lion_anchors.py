import numpy as np
from PIL import Image

chassis = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold_512.png')
mane = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/head_unit/ear_lion_gilded_mane_512.png')
costume = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/costume/costume_nutcracker_guard_512.png')
weapon = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/weapon/wpn_knight_lance_512.png')
key = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/winding_key/key_classic_brass_512.png')
core = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/optic_core/core_cyan_emerald_512.png')

print("Chassis bbox:", chassis.getbbox())
print("Mane bbox:   ", mane.getbbox())
print("Costume bbox:", costume.getbbox())
print("Weapon bbox: ", weapon.getbbox())
print("Key bbox:    ", key.getbbox())
print("Core bbox:   ", core.getbbox())

# Let's check overlap between mane and chassis
ch_a = np.array(chassis)[:, :, 3]
mn_a = np.array(mane)[:, :, 3]
overlap = (ch_a > 0) & (mn_a > 0)
y_ov, x_ov = np.where(overlap)
if len(y_ov) > 0:
    print(f"Mane & Chassis overlap: x={x_ov.min()}..{x_ov.max()} (mean {x_ov.mean():.1f}), y={y_ov.min()}..{y_ov.max()} (mean {y_ov.mean():.1f})")

# Let's check where the key shaft meets the chassis/body
k_a = np.array(key)[:, :, 3]
k_ch_overlap = (ch_a > 0) & (k_a > 0)
y_k, x_k = np.where(k_ch_overlap)
if len(y_k) > 0:
    print(f"Key & Chassis overlap: x={x_k.min()}..{x_k.max()} (mean {x_k.mean():.1f}), y={y_k.min()}..{y_k.max()} (mean {y_k.mean():.1f})")

# Let's check where the lance grip meets the hand on chassis
w_a = np.array(weapon)[:, :, 3]
# weapon grip is usually in the hand area
w_ch_overlap = (ch_a > 0) & (w_a > 0)
y_w, x_w = np.where(w_ch_overlap)
if len(y_w) > 0:
    print(f"Weapon & Chassis overlap: x={x_w.min()}..{x_w.max()} (mean {x_w.mean():.1f}), y={y_w.min()}..{y_w.max()} (mean {y_w.mean():.1f})")

# Let's check where costume aligns on chassis
cos_a = np.array(costume)[:, :, 3]
cos_ch = (ch_a > 0) & (cos_a > 0)
y_c, x_c = np.where(cos_ch)
if len(y_c) > 0:
    print(f"Costume & Chassis overlap: x={x_c.min()}..{x_c.max()} (mean {x_c.mean():.1f}), y={y_c.min()}..{y_c.max()} (mean {y_c.mean():.1f})")
