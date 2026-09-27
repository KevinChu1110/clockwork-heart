from PIL import Image
import numpy as np

key = Image.open('/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/hound/winding_key/key_hound_four_blade_antenna_gold.png')
print('Key bbox:', key.getbbox(), 'RGBA unique alphas:', np.unique(np.array(key)[:, :, 3]))

costume = Image.open('/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/hound/costume/costume_hound_space_explorer_harness.png')
print('Costume bbox:', costume.getbbox(), 'RGBA unique alphas:', np.unique(np.array(costume)[:, :, 3]))

chassis = Image.open('/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/hound/chassis/chassis_hound_polymer_astro_default.png')
print('Chassis bbox:', chassis.getbbox(), 'RGBA unique alphas:', np.unique(np.array(chassis)[:, :, 3]))
