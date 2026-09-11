import os
from PIL import Image, ImageChops

proof_dir = "/opt/side/bravesoul-game/proofs/combat_feel"
races = ["rabbit", "lion", "fox", "boar"]

for r in races:
    idle_f = os.path.join(proof_dir, f"{r}_battle_idle.png")
    atk_f = os.path.join(proof_dir, f"{r}_battle_attack_full.png")
    if os.path.exists(idle_f) and os.path.exists(atk_f):
        im_idle = Image.open(idle_f)
        im_atk = Image.open(atk_f)
        # 裁剪角色位置
        c_idle = im_idle.crop((160, 160, 520, 480))
        c_atk = im_atk.crop((160, 160, 520, 480))
        diff = ImageChops.difference(c_idle, c_atk)
        bbox = diff.getbbox()
        print(f"Race {r}: idle vs attack diff bbox={bbox}")
        # 保存對比圖
        comp = Image.new("RGB", (c_idle.width * 2, c_idle.height))
        comp.paste(c_idle, (0, 0))
        comp.paste(c_atk, (c_idle.width, 0))
        comp.save(os.path.join(proof_dir, f"{r}_idle_vs_attack_comparison.png"))
