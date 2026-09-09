#!/usr/bin/env python3
"""
produce_boar_assets.py
Generates the 11 core boar character assets for Clockwork Heart:
1. web/media/hero/boar_idle.png (128x128)
2. game/assets/sprites/player/boar_battle.png (128x128)
3-6. game/assets/sprites/player/boar_walk_{0..3}.png (64x64)
7-10. game/assets/sprites/player/boar_walk_{0..3}_x3.png (128x128)
11. game/assets/sprites/portraits/boar.png (128x128 HUD)
"""
import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
PORTRAITS_DIR = f"{REPO_ROOT}/game/assets/sprites/portraits"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"
PARTY_IDLE = f"{PLAYER_DIR}/party/boar_idle.png"
BOAR_WARRIOR = f"{PORTRAITS_DIR}/boar_warrior.png"

def build_base_idle() -> Image.Image:
    assert os.path.exists(PARTY_IDLE), f"Missing {PARTY_IDLE}"
    return Image.open(PARTY_IDLE).convert("RGBA")

def build_battle_sprite(base: Image.Image) -> Image.Image:
    W, H = base.size
    battle = base.copy()

    # Add combat enhancements:
    # 1. Cyan optical eye flare & core flare
    for y in range(H):
        for x in range(W):
            pix = battle.getpixel((x, y))
            if not isinstance(pix, tuple) or len(pix) < 4:
                continue
            r, g, b, a = pix[0], pix[1], pix[2], pix[3]
            if a == 0:
                continue
            # Eye enhancement
            if 56 <= x <= 64 and 38 <= y <= 46:
                if g > 130 and b > 130 and r < 120:
                    battle.putpixel((x, y), (min(255, r + 40), min(255, g + 60), min(255, b + 60), 255))
            # Core enhancement
            if 52 <= x <= 62 and 70 <= y <= 80:
                if g > 120 and b > 120 and r < 120:
                    battle.putpixel((x, y), (min(255, r + 30), min(255, g + 60), min(255, b + 60), 255))
            # Molten strike edge on warhammer
            if 20 <= x <= 44 and 78 <= y <= 118:
                if 70 <= r <= 150 and 60 <= g <= 130 and b < 100:
                    if x <= 26 or y <= 84 or y >= 112:
                        battle.putpixel((x, y), (min(255, r + 90), min(255, g + 45), min(255, b + 10), a))

    # Optical eye gleam
    gleam = [
        (0, 0, (180, 255, 255, 255)),
        (-1, 0, (100, 240, 255, 200)),
        (1, 0, (100, 240, 255, 200)),
        (0, -1, (100, 240, 255, 200)),
        (0, 1, (100, 240, 255, 200)),
    ]
    for dx, dy, col in gleam:
        gx, gy = 60 + dx, 41 + dy
        if 0 <= gx < W and 0 <= gy < H:
            battle.putpixel((gx, gy), col)

    return battle

def build_walk_frame(base: Image.Image, dx: int, dy: int) -> Image.Image:
    frame = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    frame.paste(base, (dx, dy), base)
    return frame

def build_hud_portrait() -> Image.Image:
    assert os.path.exists(BOAR_WARRIOR), f"Missing {BOAR_WARRIOR}"
    src = Image.open(BOAR_WARRIOR).convert("RGBA")
    # Scale to 96x96 to ensure comfortable safe margins for circular/rounded HUD frames
    inner = src.resize((96, 96), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    # Paste with +4px shift right to give left tusk breathing room
    paste_x = (128 - 96) // 2 + 4
    paste_y = (128 - 96) // 2 + 3
    canvas.paste(inner, (paste_x, paste_y), inner)
    return canvas

def main():
    print("=== Generating Boar Core Assets ===")

    # 1. web/media/hero/boar_idle.png (128x128)
    base_idle = build_base_idle()
    web_idle_path = os.path.join(WEB_HERO_DIR, "boar_idle.png")
    os.makedirs(os.path.dirname(web_idle_path), exist_ok=True)
    base_idle.save(web_idle_path, "PNG")
    print(f"✓ Saved [1/11] {web_idle_path}: size={base_idle.size}, bbox={base_idle.getbbox()}")

    # 2. game/assets/sprites/player/boar_battle.png (128x128)
    battle_sprite = build_battle_sprite(base_idle)
    battle_path = os.path.join(PLAYER_DIR, "boar_battle.png")
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
        p128 = os.path.join(PLAYER_DIR, f"boar_walk_{i}_x3.png")
        w128.save(p128, "PNG")
        print(f"✓ Saved [{3+i*2}/11] {p128}: size={w128.size}, bbox={w128.getbbox()}")

        w64 = w128.resize((64, 64), Image.Resampling.LANCZOS)
        p64 = os.path.join(PLAYER_DIR, f"boar_walk_{i}.png")
        w64.save(p64, "PNG")
        print(f"✓ Saved [{4+i*2}/11] {p64}: size={w64.size}, bbox={w64.getbbox()}")

    # 11. game/assets/sprites/portraits/boar.png (128x128 HUD)
    hud_portrait = build_hud_portrait()
    hud_path = os.path.join(PORTRAITS_DIR, "boar.png")
    hud_portrait.save(hud_path, "PNG")
    print(f"✓ Saved [11/11] {hud_path}: size={hud_portrait.size}, bbox={hud_portrait.getbbox()}")

    print("\n✓ ALL 11 BOAR ASSETS SUCCESSFULLY PRODUCED AND SAVED!")

if __name__ == "__main__":
    main()
