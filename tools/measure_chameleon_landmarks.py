from PIL import Image
import numpy as np

base_dir = "game/assets/sprites/player/paperdoll/chameleon"
comp = Image.open(f"{base_dir}/proof_paperdoll_chameleon_composite.png").convert("RGBA")
arr = np.array(comp)

# Find center of optic_core
optic = Image.open(f"{base_dir}/optic_core/face_chameleon_turret_rangefinder_lens.png").convert("RGBA")
o_arr = np.array(optic)
ys, xs = np.where(o_arr[:, :, 3] > 100)
print(f"Optic core: x in [{xs.min()}, {xs.max()}], y in [{ys.min()}, {ys.max()}]")
left_eye = o_arr[:, :64, 3] > 100
right_eye = o_arr[:, 64:, 3] > 100
ly, lx = np.where(left_eye)
ry, rx = np.where(right_eye)
rx += 64
print(f"Left eye center: ({lx.mean():.1f}, {ly.mean():.1f})")
print(f"Right eye center: ({rx.mean():.1f}, {ry.mean():.1f})")

# Find weapon grip center
wpn = Image.open(f"{base_dir}/weapon/weapon_chameleon_mirage_compound_bow.png").convert("RGBA")
w_arr = np.array(wpn)
wys, wxs = np.where(w_arr[:, :, 3] > 50)
print(f"Weapon bbox: ({wxs.min()}, {wys.min()}, {wxs.max()}, {wys.max()})")
print(f"Weapon center: ({wxs.mean():.1f}, {wys.mean():.1f})")

# Curio tail center
curio = Image.open(f"{base_dir}/back_curio/curio_chameleon_spiral_torsion_tail.png").convert("RGBA")
c_arr = np.array(curio)
cys, cxs = np.where(c_arr[:, :, 3] > 50)
print(f"Curio center: ({cxs.mean():.1f}, {cys.mean():.1f})")

# Key center
key = Image.open(f"{base_dir}/winding_key/key_chameleon_prismatic_trivane.png").convert("RGBA")
k_arr = np.array(key)
kys, kxs = np.where(k_arr[:, :, 3] > 50)
print(f"Key center: ({kxs.mean():.1f}, {kys.mean():.1f})")
