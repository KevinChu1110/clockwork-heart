from PIL import Image
import numpy as np

comp = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/sailfish/proof_paperdoll_sailfish_composite.png")
arr = np.array(comp)

# Look at optic core around (42..88, 36..52)
optic_zone = arr[36:52, 42:88]
optic_opaque = optic_zone[:, :, 3] > 8
optic_colors = len(np.unique(optic_zone[optic_opaque][:, :3], axis=0))
print(f"Optic zone [36:52, 42:88] unique colors: {optic_colors}")

# Check ultra-dark pixels in composite
alpha = arr[:, :, 3]
rgb = arr[:, :, :3]
dark_mask = (alpha > 50) & (rgb[:, :, 0] < 10) & (rgb[:, :, 1] < 10) & (rgb[:, :, 2] < 10)
print(f"Composite ultra dark (<10) count: {np.sum(dark_mask)}")
