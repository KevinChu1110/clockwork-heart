# Coordinate mapping between PlayerBody in battle.tscn and 128x128 sprite
# In battle.tscn:
# PlayerSlot is in Arena.
# In f0010 (idle):
# We know:
# Steel pixels in f0010: X in [255..367], Y in [380..417]
# And in 128x128 idle sprite:
# Ivory belly/arms: X in [27..102], Y in [13..119]
# Let's verify the exact scale and offset!

from PIL import Image
import numpy as np

f10 = Image.open("/opt/side/bravesoul-game/proofs/macaque_frames/f_0010.png").convert("RGBA")
comp = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/proof_paperdoll_macaque_composite.png").convert("RGBA")

# Let's find the exact scale and position of PlayerBody on screen
# By finding template match of comp on f10
arr_f = np.array(f10)
arr_c = np.array(comp)

# In PlayerSlot, custom_minimum_size is (200, 250).
# stretch_mode is STRETCH_KEEP_ASPECT_CENTERED.
# Since comp is 128x128 (aspect 1:1), in (200, 250) the texture is scaled to 200x200!
# Scale factor = 200 / 128 = 1.5625!
scale = 200.0 / 128.0
print(f"Scale: {scale}")

# If scaled to 200x200:
# Where is the top-left corner of the 200x200 texture in f10?
# In f10, steel Y in [380..417].
# In comp (128x128), where are those steel pixels?
# Let's find which Y in comp have steel:
steel_comp = (arr_c[:, :, 3] > 128) & (arr_c[:, :, 0] > 185) & (arr_c[:, :, 1] > 185) & (arr_c[:, :, 2] > 185)
ys_c, xs_c = np.where(steel_comp)
print(f"comp steel Y: [{ys_c.min()}..{ys_c.max()}], X: [{xs_c.min()}..{xs_c.max()}]")
# In comp, steel Y is [19..120]!
# If comp is at top-left (X0, Y0) and scaled by 1.5625:
# Screen Y = Y0 + comp_Y * 1.5625
# If comp_Y=120 -> Screen Y ~= 417
# Then Y0 + 120 * 1.5625 = 417 => Y0 + 187.5 = 417 => Y0 ~= 229.5!
# And for X: comp_X=101 -> Screen X ~= 367 => X0 + 101 * 1.5625 = 367 => X0 + 157.8 = 367 => X0 ~= 209!
print(f"Estimated PlayerBody texture rect on screen: X in [209, 409], Y in [230, 430]")
