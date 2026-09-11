import os
from PIL import Image, ImageChops

base_im = Image.open("proofs/combat_feel/tmp_10s/frame_010.png")
# 角色區域 (x: 180~520, y: 180~480)
c_base_p = base_im.crop((180, 180, 520, 480))
# 敵方跳字區域 (x: 750~1150, y: 100~450)
c_base_e = base_im.crop((750, 100, 1150, 450))

p_diffs = []
e_diffs = []

for i in range(1, 301):
    cur_im = Image.open(f"proofs/combat_feel/tmp_10s/frame_{i:03d}.png")
    cp = cur_im.crop((180, 180, 520, 480))
    ce = cur_im.crop((750, 100, 1150, 450))
    
    dp = ImageChops.difference(c_base_p, cp)
    de = ImageChops.difference(c_base_e, ce)
    
    stat_p = sum(list(dp.convert("L").getdata()))
    stat_e = sum(list(de.convert("L").getdata()))
    
    if stat_p > 0:
        p_diffs.append((i, stat_p))
    if stat_e > 0:
        e_diffs.append((i, stat_e))

# 找出角色位移最大峰值（Lunge 頂點）
p_diffs.sort(key=lambda x: x[1], reverse=True)
print("Top 5 Player Lunge Peak Frames:")
for f, s in p_diffs[:5]:
    print(f"  Frame {f:03d}: diff_sum={s}")

# 找出敵方跳字/受擊最大峰值（Damage / Break 頂點）
e_diffs.sort(key=lambda x: x[1], reverse=True)
print("Top 10 Enemy Hit / Float Peak Frames:")
for f, s in e_diffs[:10]:
    print(f"  Frame {f:03d}: diff_sum={s}")
