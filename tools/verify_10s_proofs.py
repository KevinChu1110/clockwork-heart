from PIL import Image, ImageChops

im_a = Image.open("proofs/combat_feel/frame_a_idle.png")
im_b = Image.open("proofs/combat_feel/frame_b_lunge_attack.png")
im_c = Image.open("proofs/combat_feel/frame_c_damage_float.png")
im_d = Image.open("proofs/combat_feel/frame_d_break_part.png")

# (a) 比較角色區域位移
c_a = im_a.crop((180, 180, 520, 480))
c_b = im_b.crop((180, 180, 520, 480))
diff_ab = ImageChops.difference(c_a, c_b)
print("(a) Lunge difference bbox in player area:", diff_ab.getbbox())

# 生成對比圖
comp_ab = Image.new("RGB", (c_a.width * 2 + 10, c_a.height), (20, 20, 20))
comp_ab.paste(c_a, (0, 0))
comp_ab.paste(c_b, (c_a.width + 10, 0))
comp_ab.save("proofs/combat_feel/proof_lunge_comparison_10s.png")

# (b) 傷害跳字區域 (x: 750~1150, y: 150~450)
c_c = im_c.crop((750, 150, 1150, 450))
c_c.save("proofs/combat_feel/proof_damage_crop_10s.png")

# (c) 部位破壞 BREAK 區域 (x: 750~1150, y: 180~480)
c_d = im_d.crop((750, 180, 1150, 480))
c_d.save("proofs/combat_feel/proof_break_crop_10s.png")
print("Saved all 10s proof crops.")
