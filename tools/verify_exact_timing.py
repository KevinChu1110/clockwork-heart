import os
from PIL import Image, ImageChops

proof_dir = "/opt/side/bravesoul-game/proofs/combat_feel"
tmp_dir = os.path.join(proof_dir, "tmp_10s")

f_idle = os.path.join(tmp_dir, "frame_009.png")
f_lunge = os.path.join(tmp_dir, "frame_021.png")
f_hit = os.path.join(tmp_dir, "frame_024.png")
f_break = os.path.join(tmp_dir, "frame_097.png")

im_idle = Image.open(f_idle)
im_lunge = Image.open(f_lunge)
im_hit = Image.open(f_hit)
im_break = Image.open(f_break)

# 1. 檢驗 (a) 角色位移
c_idle = im_idle.crop((180, 180, 520, 480))
c_lunge = im_lunge.crop((180, 180, 520, 480))
diff_lunge = ImageChops.difference(c_idle, c_lunge)
print("(a) Lunge difference bbox in player area:", diff_lunge.getbbox())

# 2. 檢驗 (b) 傷害跳字 (x: 750~1100, y: 60~300)
c_hit = im_hit.crop((750, 60, 1100, 300))
diff_hit = ImageChops.difference(im_idle.crop((750, 60, 1100, 300)), c_hit)
print("(b) Damage float difference bbox:", diff_hit.getbbox())

# 3. 檢驗 (c) BREAK 部位破壞跳字
c_break = im_break.crop((750, 60, 1100, 350))
diff_break = ImageChops.difference(im_idle.crop((750, 60, 1100, 350)), c_break)
print("(c) BREAK float difference bbox:", diff_break.getbbox())

# 保存這些裁剪證明
c_lunge.save(os.path.join(proof_dir, "verified_lunge_player.png"))
c_hit.save(os.path.join(proof_dir, "verified_damage_float.png"))
c_break.save(os.path.join(proof_dir, "verified_break_float.png"))
