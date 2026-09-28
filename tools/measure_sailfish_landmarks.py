from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/sailfish"

slices = {
    "key": f"{BASE_DIR}/winding_key/key_sailfish_abyssal_helm_trident.png",
    "curio": f"{BASE_DIR}/back_curio/curio_sailfish_clockwork_sailfin_mantle.png",
    "chassis": f"{BASE_DIR}/chassis/chassis_sailfish_abyssal_titanium_default.png",
    "head": f"{BASE_DIR}/head_unit/head_sailfish_hydrofoil_visor_crest.png",
    "costume": f"{BASE_DIR}/costume/costume_sailfish_abyssal_knight_cuirass.png",
    "optic": f"{BASE_DIR}/optic_core/face_sailfish_dual_abyssal_optic_lens.png",
    "weapon": f"{BASE_DIR}/weapon/weapon_sailfish_hydrofoil_lance.png",
}

for name, path in slices.items():
    im = Image.open(path)
    arr = np.array(im)
    alpha = arr[:, :, 3]
    ys, xs = np.where(alpha > 30)
    print(f"=== {name} ===")
    print(f"  bbox: ({np.min(xs)}, {np.min(ys)}, {np.max(xs)+1}, {np.max(ys)+1})")
    print(f"  center: ({np.mean(xs):.1f}, {np.mean(ys):.1f})")

# Specifically check optic lens
optic_arr = np.array(Image.open(slices["optic"]))
ys, xs = np.where(optic_arr[:, :, 3] > 30)
# Check left and right lens centers
left_mask = (optic_arr[:, :, 3] > 30) & (np.arange(128)[None, :] < 64)
right_mask = (optic_arr[:, :, 3] > 30) & (np.arange(128)[None, :] >= 64)
ly, lx = np.where(left_mask)
ry, rx = np.where(right_mask)
print(f"Optic left eye center: ({np.mean(lx):.1f}, {np.mean(ly):.1f})")
print(f"Optic right eye center: ({np.mean(rx):.1f}, {np.mean(ry):.1f})")

# Check weapon lance
wpn_arr = np.array(Image.open(slices["weapon"]))
ys, xs = np.where(wpn_arr[:, :, 3] > 30)
print(f"Weapon center: ({np.mean(xs):.1f}, {np.mean(ys):.1f})")
print(f"Weapon tip / grip info: x in [{np.min(xs)}..{np.max(xs)}], y in [{np.min(ys)}..{np.max(ys)}]")

# Check key
key_arr = np.array(Image.open(slices["key"]))
ys, xs = np.where(key_arr[:, :, 3] > 30)
print(f"Key center: ({np.mean(xs):.1f}, {np.mean(ys):.1f})")
print(f"Key y min: {np.min(ys)}, max: {np.max(ys)}")
