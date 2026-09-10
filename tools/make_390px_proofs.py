import os
from PIL import Image

shot_dir = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_bb7cec3d/screenshots"
idle_path = os.path.join(shot_dir, "proof_battle_lion_full_screen.png")
atk_path = os.path.join(shot_dir, "proof_battle_lion_attack_full_screen.png")

# Generate 390px wide versions (Rule 16 mobile verification standard)
for src, name in [(idle_path, "proof_battle_lion_full_screen_390px.png"), (atk_path, "proof_battle_lion_attack_full_screen_390px.png")]:
    im = Image.open(src)
    w, h = im.size
    ratio = 390.0 / float(w)
    new_h = int(h * ratio)
    im_390 = im.resize((390, new_h), Image.Resampling.LANCZOS)
    out_p = os.path.join(shot_dir, name)
    im_390.save(out_p)
    print(f"Saved {name}: {im_390.size}")
