#!/usr/bin/env python3
"""
produce_lion_assets.py
Generates the 11 core lion character assets for Clockwork Heart:
1. web/media/hero/lion_idle.png (128x128)
2. game/assets/sprites/player/lion_battle.png (128x128)
3-6. game/assets/sprites/player/lion_walk_{0..3}.png (64x64)
7-10. game/assets/sprites/player/lion_walk_{0..3}_x3.png (128x128)
11. game/assets/sprites/portraits/lion.png (128x128)
"""
import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
LION_PAPERDOLL = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/lion"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
PORTRAITS_DIR = f"{REPO_ROOT}/game/assets/sprites/portraits"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

def load_slice(slot: str, fn: str) -> Image.Image:
    p = os.path.join(LION_PAPERDOLL, slot, fn)
    return Image.open(p).convert("RGBA")

def build_base_composite() -> Image.Image:
    comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    # Z-index ascending order:
    # 1. winding_key (Z: 5)
    comp.alpha_composite(load_slice("winding_key", "key_classic_brass.png"))
    # 2. back_curio (Z: 8)
    comp.alpha_composite(load_slice("back_curio", "curio_lion_fan_tail.png"))
    # 3. chassis (Z: 10)
    comp.alpha_composite(load_slice("chassis", "paint_brass_gold.png"))
    # 4. head_unit (Z: 20)
    comp.alpha_composite(load_slice("head_unit", "ear_lion_gilded_mane.png"))
    # 5. costume (Z: 25)
    comp.alpha_composite(load_slice("costume", "costume_nutcracker_guard.png"))
    # 6. optic_core (Z: 30)
    comp.alpha_composite(load_slice("optic_core", "core_cyan_emerald.png"))
    # 7. weapon (Z: 40)
    comp.alpha_composite(load_slice("weapon", "wpn_knight_lance.png"))
    return comp

def build_battle_sprite() -> Image.Image:
    key = load_slice("winding_key", "key_classic_brass.png")
    tail = load_slice("back_curio", "curio_lion_fan_tail.png")
    chassis = load_slice("chassis", "paint_brass_gold.png")
    head = load_slice("head_unit", "ear_lion_gilded_mane.png")
    costume = load_slice("costume", "costume_nutcracker_guard.png")
    core = load_slice("optic_core", "core_cyan_emerald.png")
    lance = load_slice("weapon", "wpn_knight_lance.png")

    # Rotate lance around grip (32, 88) by 10 degrees forward into combat ready angle
    pad = 128
    big = Image.new("RGBA", (128 + pad * 2, 128 + pad * 2), (0, 0, 0, 0))
    big.paste(lance, (pad, pad), lance)
    rot = big.rotate(10, resample=Image.Resampling.BICUBIC, center=(pad + 32, pad + 88))
    lance_rot = rot.crop((pad, pad, pad + 128, pad + 128))

    lance_final = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    lance_final.paste(lance_rot, (1, 2), lance_rot)

    comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    # 1. Key
    comp.alpha_composite(key)
    # 2. Tail braced
    tail_braced = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tail_braced.paste(tail, (-1, 0), tail)
    comp.alpha_composite(tail_braced)

    # 3. Chassis: separate ground shadow and body
    chassis_body = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    chassis_shadow = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    c_pix = chassis.load()
    cb_pix = chassis_body.load()
    cs_pix = chassis_shadow.load()

    for y in range(128):
        for x in range(128):
            a = c_pix[x, y][3]
            if a > 0:
                if y >= 118 and c_pix[x, y][0] < 200 and c_pix[x, y][1] < 190 and c_pix[x, y][2] < 170:
                    cs_pix[x, y] = c_pix[x, y]
                else:
                    cb_pix[x, y] = c_pix[x, y]

    # Ground shadow firmly anchored
    comp.alpha_composite(chassis_shadow)

    # Body braced with combat tension: dx=-1, dy=1
    body_shifted = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    body_shifted.paste(chassis_body, (-1, 1), chassis_body)
    comp.alpha_composite(body_shifted)

    # Head shifted (-1, 1)
    head_shifted = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    head_shifted.paste(head, (-1, 1), head)
    comp.alpha_composite(head_shifted)

    # Costume shifted (-1, 1)
    costume_shifted = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    costume_shifted.paste(costume, (-1, 1), costume)
    comp.alpha_composite(costume_shifted)

    # Core shifted (-1, 1)
    core_shifted = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    core_shifted.paste(core, (-1, 1), core)
    comp.alpha_composite(core_shifted)

    # Rotated lance
    comp.alpha_composite(lance_final)
    return comp

def build_walk_frame(base: Image.Image, dx: int, dy: int) -> Image.Image:
    frame = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    frame.paste(base, (dx, dy), base)
    return frame

def main():
    print("=== Generating Lion Core Assets ===")

    # 1. web/media/hero/lion_idle.png (128x128)
    base_idle = build_base_composite()
    web_idle_path = os.path.join(WEB_HERO_DIR, "lion_idle.png")
    os.makedirs(os.path.dirname(web_idle_path), exist_ok=True)
    base_idle.save(web_idle_path, "PNG")
    print(f"✓ Saved [1/11] {web_idle_path}: size={base_idle.size}, bbox={base_idle.getbbox()}")

    # 2. game/assets/sprites/player/lion_battle.png (128x128)
    battle_sprite = build_battle_sprite()
    battle_path = os.path.join(PLAYER_DIR, "lion_battle.png")
    os.makedirs(os.path.dirname(battle_path), exist_ok=True)
    battle_sprite.save(battle_path, "PNG")
    print(f"✓ Saved [2/11] {battle_path}: size={battle_sprite.size}, bbox={battle_sprite.getbbox()}")

    # 3-10. Walk frames (0..3): 128x128 (_x3) and 64x64
    walk_shifts = [
        (2, 0),   # Frame 0: Stride forward / right
        (0, -3),  # Frame 1: Up-bob passing
        (-2, 1),  # Frame 2: Stride back / left
        (0, 1),   # Frame 3: Down-bob passing
    ]

    for i, (dx, dy) in enumerate(walk_shifts):
        w128 = build_walk_frame(base_idle, dx, dy)
        p128 = os.path.join(PLAYER_DIR, f"lion_walk_{i}_x3.png")
        w128.save(p128, "PNG")
        print(f"✓ Saved [{3+i*2}/11] {p128}: size={w128.size}, bbox={w128.getbbox()}")

        w64 = w128.resize((64, 64), Image.Resampling.LANCZOS)
        p64 = os.path.join(PLAYER_DIR, f"lion_walk_{i}.png")
        w64.save(p64, "PNG")
        print(f"✓ Saved [{4+i*2}/11] {p64}: size={w64.size}, bbox={w64.getbbox()}")

    # 11. game/assets/sprites/portraits/lion.png (128x128 HUD)
    dialogue_portrait_p = os.path.join(PORTRAITS_DIR, "lion_knight.png")
    assert os.path.exists(dialogue_portrait_p), f"Missing {dialogue_portrait_p}"
    dp = Image.open(dialogue_portrait_p)
    hud_portrait = dp.resize((128, 128), Image.Resampling.LANCZOS)
    hud_path = os.path.join(PORTRAITS_DIR, "lion.png")
    hud_portrait.save(hud_path, "PNG")
    print(f"✓ Saved [11/11] {hud_path}: size={hud_portrait.size}, bbox={hud_portrait.getbbox()}")

    print("\n✓ ALL 11 ASSETS SUCCESSFULLY PRODUCED AND SAVED!")

if __name__ == "__main__":
    main()
