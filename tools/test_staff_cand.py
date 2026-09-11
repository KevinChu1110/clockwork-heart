import os
import sys
from PIL import Image

sys.path.insert(0, "/opt/side/bravesoul-game/tools")
from verify_fox_action_poses import measure_staff_linearity, measure_shadow_rows

cand = Image.open("/tmp/test_attack_candidate.png").convert("RGBA")
st_resid = measure_staff_linearity(cand)
sh_rows = measure_shadow_rows(cand)
print(f"staff_linearity max_resid = {st_resid:.2f} px")
print(f"shadow profile = {sh_rows}")
