from PIL import Image, ImageDraw, ImageFilter
import numpy as np

BASE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/cat"
optic = Image.open(f"{BASE_DIR}/optic_core/face_cat_slit_optic_emerald.png").convert("RGBA")
optic_arr = np.array(optic)

# Mask of existing eye pixels
mask = optic_arr[:, :, 3] > 20

# Create hit squint eye layer
hit_optic = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
# Fill socket area with dark plate
h_arr = np.array(hit_optic)
h_arr[mask] = [30, 32, 42, 255] # dark socket plate
hit_optic = Image.fromarray(h_arr)

draw = ImageDraw.Draw(hit_optic)
# Draw sharp impact squint "> <"
# Left eye ">":
draw.line([(48, 37), (55, 40)], fill=(78, 216, 106, 255), width=2)
draw.line([(48, 43), (55, 40)], fill=(78, 216, 106, 255), width=2)
draw.line([(49, 38), (54, 40)], fill=(255, 255, 230, 255), width=1)
draw.line([(49, 42), (54, 40)], fill=(255, 255, 230, 255), width=1)

# Right eye "<":
draw.line([(79, 37), (72, 40)], fill=(78, 216, 106, 255), width=2)
draw.line([(79, 43), (72, 40)], fill=(78, 216, 106, 255), width=2)
draw.line([(78, 38), (73, 40)], fill=(255, 255, 230, 255), width=1)
draw.line([(78, 42), (73, 40)], fill=(255, 255, 230, 255), width=1)

hit_optic.save("/opt/side/bravesoul-game/tools/test_hit_optic.png")
print("Saved test_hit_optic.png")
