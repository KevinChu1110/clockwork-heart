from PIL import Image
import numpy as np

# Let's inspect the pixels of comp at y in [83, 120]
comp = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/proof_paperdoll_macaque_composite.png").convert("RGBA")
arr_c = np.array(comp)

# In atk, let's copy the lower body / legs / claws from comp or composite with proper lunge
# In lunge:
# The lead leg lunges forward (x: 60..90, y: 80..112)
# The rear leg braces back (x: 28..55, y: 80..112)
# Both legs have the ivory white plates and steel kneecaps/shin guards!
# And the claw gauntlets:
# Rear hand holds the downward/rear claw gauntlet (x: 25..45, y: 75..105)
# Lead hand has the forward/downward slashing claw gauntlet (x: 80..125, y: 55..95)

# Let's see: if we ensure in atk that:
# 1. Ivory thighs, shins, knee joints have steel tone in y in [80..110]
# 2. Rear claw gauntlet blades span y in [80..105]
# 3. Slashing claw blades span down into y in [80..95]
# Let's calculate the steel count!
