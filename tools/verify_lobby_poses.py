from PIL import Image, ImageChops
import os

print("=== 1. 檢驗各族大廳原始資產貼圖（PIL ImageChops diff 驗證）===")
races = ["rabbit", "lion", "fox", "macaque", "boar"]
base_dir = "/opt/side/bravesoul-game/game/assets/sprites/player"

for race in races:
    if race == "rabbit":
        idle_path = f"{base_dir}/rabbit_idle_x3.png"
        atk_path = f"{base_dir}/poses/attack.png"
    else:
        idle_path = f"{base_dir}/poses/{race}/idle.png"
        atk_path = f"{base_dir}/poses/{race}/attack.png"

    assert os.path.exists(idle_path), f"找不到 {idle_path}"
    assert os.path.exists(atk_path), f"找不到 {atk_path}"

    img_idle = Image.open(idle_path).convert("RGBA")
    img_atk = Image.open(atk_path).convert("RGBA")

    diff = ImageChops.difference(img_idle, img_atk)
    bbox = diff.getbbox(alpha_only=False)
    assert bbox is not None, f"種族 {race} 的 idle 與 attack pixel diff 為 0！"
    print(f"  [{race}] idle vs attack diff bbox: {bbox} (非 None, 差異非 0)")

print("\n=== 2. 檢驗大廳實機截圖 (Captured Screenshots diff 驗證) ===")
shot_dir = "/opt/side/bravesoul-game/screenshots"

# 獅子實機截圖比較
lion_idle_shot = Image.open(f"{shot_dir}/proof_lobby_lion_idle.png").convert("RGBA")
lion_atk_shot = Image.open(f"{shot_dir}/proof_lobby_lion_attack.png").convert("RGBA")
lion_diff = ImageChops.difference(lion_idle_shot, lion_atk_shot)
lion_bbox = lion_diff.getbbox(alpha_only=False)
assert lion_bbox is not None, "獅子大廳待機與攻擊實機截圖完全相同 (diff is None)！"
print(f"  [實機截圖 獅子] idle vs attack diff bbox: {lion_bbox} (非 None)")

# 狐狸實機截圖比較
fox_idle_shot = Image.open(f"{shot_dir}/proof_lobby_fox_idle.png").convert("RGBA")
fox_atk_shot = Image.open(f"{shot_dir}/proof_lobby_fox_attack.png").convert("RGBA")
fox_diff = ImageChops.difference(fox_idle_shot, fox_atk_shot)
fox_bbox = fox_diff.getbbox(alpha_only=False)
assert fox_bbox is not None, "狐狸大廳待機與攻擊實機截圖完全相同 (diff is None)！"
print(f"  [實機截圖 狐狸] idle vs attack diff bbox: {fox_bbox} (非 None)")

print("\nALL VERIFICATIONS PASSED: 五族姿勢及實機戳碰差異均非 0！")
