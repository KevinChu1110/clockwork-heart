import os
from PIL import Image, ImageChops

proof_dir = "/opt/side/bravesoul-game/proofs/combat_feel"
races = ["rabbit", "lion", "fox", "boar"]

for r in races:
    p1 = os.path.join(proof_dir, f"{r}_proof_01_idle.png")
    p2 = os.path.join(proof_dir, f"{r}_proof_02_attack_lunge.png")
    p3 = os.path.join(proof_dir, f"{r}_proof_03_damage_hit.png")
    p4 = os.path.join(proof_dir, f"{r}_proof_04_break.png")

    im1 = Image.open(p1)
    im2 = Image.open(p2)
    im3 = Image.open(p3)
    im4 = Image.open(p4)

    # (a) 角色位置對比 (x: 140~520, y: 160~480)
    c1 = im1.crop((140, 160, 520, 480))
    c2 = im2.crop((140, 160, 520, 480))
    diff = ImageChops.difference(c1, c2)
    print(f"[{r}] (a) Pos diff bbox: {diff.getbbox()}")

    comp = Image.new("RGB", (c1.width * 2 + 10, c1.height), (30, 30, 30))
    comp.paste(c1, (0, 0))
    comp.paste(c2, (c1.width + 10, 0))
    comp.save(os.path.join(proof_dir, f"proof_a_lunge_comparison_{r}.png"))

    # (b) 傷害跳字 (x: 750~1150, y: 120~420)
    c3 = im3.crop((750, 120, 1150, 420))
    c3.save(os.path.join(proof_dir, f"proof_b_damage_{r}.png"))

    # (b-2) BREAK 部位破壞跳字 (x: 750~1150, y: 160~460)
    c4 = im4.crop((750, 160, 1150, 460))
    c4.save(os.path.join(proof_dir, f"proof_b_break_{r}.png"))

    # (c) 不是空手：手部與軀幹放大 (x: 220~460, y: 180~460)
    c_weapon = im2.crop((220, 180, 460, 460))
    try:
        resample = Image.Resampling.NEAREST
    except AttributeError:
        resample = Image.NEAREST
    c_w_4x = c_weapon.resize((c_weapon.width * 3, c_weapon.height * 3), resample)
    c_w_4x.save(os.path.join(proof_dir, f"proof_c_weapon_{r}.png"))
    print(f"[{r}] Saved all proof crops.")
