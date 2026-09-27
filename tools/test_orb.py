from PIL import Image, ImageDraw
import numpy as np

p = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/owl/back_curio/curio_owl_floating_micro_orrery.png"
im = Image.open(p).convert("RGBA")
arr = np.array(im)

cx, cy = 107.0, 61.0
r = 17.5

mask = Image.new("L", (128, 128), 0)
m_draw = ImageDraw.Draw(mask)
m_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)

# Circular brass bezel rim
rim = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
r_draw = ImageDraw.Draw(rim)
r_draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 208, 40, 240), width=1)
r_draw.ellipse([cx - r - 1, cy - r - 1, cx + r + 1, cy + r + 1], outline=(31, 26, 58, 220), width=1)

orb = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
orb.paste(im, (0, 0), mask)
orb = Image.alpha_composite(orb, rim)

bb = orb.getbbox()
print("Orb bbox:", bb)

# Check audit metrics
o_arr = np.array(orb)
alpha = o_arr[:, :, 3]
opaque_mask = alpha > 8
opaque_count = int(np.sum(opaque_mask))
opaque_rgb = o_arr[opaque_mask][:, :3]
unique_colors = len(np.unique(opaque_rgb, axis=0))
c100 = (unique_colors / opaque_count) * 100.0
print(f"Opaque Pixels: {opaque_count}, Unique Colors: {unique_colors}, c100: {c100:.2f}%")
