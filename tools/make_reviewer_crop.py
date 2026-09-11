import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
atk = Image.open(f"{REPO_ROOT}/proofs/macaque_test/candidate_attack_pose.png").convert("RGBA")

# Torso + both hands:
# Macaque attack sprite bbox is (19, 12, 123, 108).
# Head is y=12..45. Torso + hands is y=42..88, x=18..124.
# Let's crop torso + both hands:
crop_torso_hands = atk.crop((18, 42, 124, 88))
# Rescale to 128px width (maintaining aspect ratio or into 128x128)
w, h = crop_torso_hands.size
scale = 128.0 / float(w)
target_h = int(round(h * scale))
resized = crop_torso_hands.resize((128, target_h), Image.Resampling.LANCZOS)

canvas_128 = Image.new("RGBA", (128, 128), (35, 30, 45, 255))
offset_y = (128 - target_h) // 2
canvas_128.paste(resized, (0, offset_y), resized)

out_path = f"{REPO_ROOT}/proofs/macaque_test/torso_hands_128px.png"
canvas_128.save(out_path)
print("Saved 128px torso+hands crop to:", out_path)
