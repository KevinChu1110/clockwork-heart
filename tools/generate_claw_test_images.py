import os
from PIL import Image
from craft_macaque_claws_complete import build_idle_paperdoll_claws, build_attack_pose_with_claws

REPO_ROOT = "/opt/side/bravesoul-game"
OUTPUT_DIR = "/opt/side/bravesoul-game/proofs/macaque_test"
os.makedirs(OUTPUT_DIR, exist_ok=True)

idle_claws = build_idle_paperdoll_claws()
atk_pose, wep_layer = build_attack_pose_with_claws()

# Save candidate files in proofs
idle_claws_path = f"{OUTPUT_DIR}/candidate_idle_claws.png"
atk_pose_path = f"{OUTPUT_DIR}/candidate_attack_pose.png"
wep_layer_path = f"{OUTPUT_DIR}/candidate_wep_layer.png"

idle_claws.save(idle_claws_path)
atk_pose.save(atk_pose_path)
wep_layer.save(wep_layer_path)

# Crop torso + hands from attack pose
# Character bbox in attack is (19, 12, 123, 108)
# Torso + hands crop: x from 16 to 125, y from 35 to 90
torso_hands = atk_pose.crop((16, 35, 125, 90))
torso_hands_path = f"{OUTPUT_DIR}/torso_hands_crop.png"
torso_hands.save(torso_hands_path)

# 128px player scale version on dark background
canvas_128 = Image.new("RGBA", (128, 128), (35, 30, 45, 255))
# Place cropped torso+hands centered or place full sprite
canvas_128.paste(atk_pose, (0, 0), atk_pose)
test_128_path = f"{OUTPUT_DIR}/attack_pose_128px.png"
canvas_128.save(test_128_path)

# 3x zoom of hand & weapon on dark background
hand_crop = atk_pose.crop((70, 45, 125, 75))
hand_3x = hand_crop.resize((hand_crop.width * 3, hand_crop.height * 3), Image.Resampling.NEAREST)
bg_3x = Image.new("RGBA", hand_3x.size, (35, 30, 45, 255))
bg_3x.paste(hand_3x, (0, 0), hand_3x)
test_3x_path = f"{OUTPUT_DIR}/attack_hand_claws_3x.png"
bg_3x.save(test_3x_path)

print("Generated test images:")
print("  Full attack sprite:", atk_pose_path)
print("  128px scale:", test_128_path)
print("  3x hand & claws crop:", test_3x_path)
