from PIL import Image
import sys

sys.path.insert(0, "/opt/side/bravesoul-game/tools")
from verify_fox_action_poses import measure_staff_linearity, measure_shadow_rows

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/attack.png").convert("RGBA")
st_resid = measure_staff_linearity(im)
sh_rows = measure_shadow_rows(im)
print(f"staff_linearity max_resid: {st_resid:.2f} px")
print(f"shadow profile: {sh_rows}")
