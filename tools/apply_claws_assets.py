import os
from craft_macaque_claws_complete import build_idle_paperdoll_claws, build_attack_pose_with_claws

REPO_ROOT = "/opt/side/bravesoul-game"

# 1. Update wpn_spring_claws.png
claws_path = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque/weapon/wpn_spring_claws.png"
idle_claws = build_idle_paperdoll_claws()
idle_claws.save(claws_path)
print("Updated:", claws_path)

# 2. Update attack.png
atk_path = f"{REPO_ROOT}/game/assets/sprites/player/poses/macaque/attack.png"
atk_pose, _ = build_attack_pose_with_claws()
atk_pose.save(atk_path)
print("Updated:", atk_path)
