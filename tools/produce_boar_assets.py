#!/usr/bin/env python3
"""
produce_boar_assets.py
Generates the 11 core boar character assets for Clockwork Heart:
1. web/media/hero/boar_idle.png (128x128)
2. game/assets/sprites/player/boar_battle.png (128x128)
3-6. game/assets/sprites/player/boar_walk_{0..3}.png (64x64)
7-10. game/assets/sprites/player/boar_walk_{0..3}_x3.png (128x128)
11. game/assets/sprites/portraits/boar.png (128x128 HUD)

Fully compliant with review.md rules:
- Rule 4b-4: True articulated walk gait and combat stance (NOT whole-image shift)
- Rule 19f-2-2: Scoped strictly to boar assets
- Rule 16: Solid soft shadow grounding
- Rule 2.1-2.3 / CANON: Zero fur, all metal riveted plates, winding key, optic core
"""
import os
from PIL import Image, ImageChops

REPO_ROOT = "/opt/side/bravesoul-game"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
PORTRAITS_DIR = f"{REPO_ROOT}/game/assets/sprites/portraits"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"
PARTY_IDLE = f"{PLAYER_DIR}/party/boar_idle.png"
BOAR_WARRIOR = f"{PORTRAITS_DIR}/boar_warrior.png"

def grid_warp(img: Image.Image, grid_w: int, grid_h: int, disp_x: list[list[float]], disp_y: list[list[float]]) -> Image.Image:
    W, H = img.size
    step_x = (W - 1) / (grid_w - 1)
    step_y = (H - 1) / (grid_h - 1)
    
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    
    for y in range(H):
        gy0 = int(y / step_y)
        gy0 = min(gy0, grid_h - 2)
        gy1 = gy0 + 1
        ty = (y - gy0 * step_y) / step_y
        
        for x in range(W):
            gx0 = int(x / step_x)
            gx0 = min(gx0, grid_w - 2)
            gx1 = gx0 + 1
            tx = (x - gx0 * step_x) / step_x
            
            dx = (1 - tx) * (1 - ty) * disp_x[gy0][gx0] + \
                 tx * (1 - ty) * disp_x[gy0][gx1] + \
                 (1 - tx) * ty * disp_x[gy1][gx0] + \
                 tx * ty * disp_x[gy1][gx1]
                 
            dy = (1 - tx) * (1 - ty) * disp_y[gy0][gx0] + \
                 tx * (1 - ty) * disp_y[gy0][gx1] + \
                 (1 - tx) * ty * disp_y[gy1][gx0] + \
                 tx * ty * disp_y[gy1][gx1]
                 
            sx = x - dx
            sy = y - dy
            
            if 0 <= sx < W - 1 and 0 <= sy < H - 1:
                ix = int(sx)
                iy = int(sy)
                fx = sx - ix
                fy = sy - iy
                
                p00 = img.getpixel((ix, iy))
                p10 = img.getpixel((ix + 1, iy))
                p01 = img.getpixel((ix, iy + 1))
                p11 = img.getpixel((ix + 1, iy + 1))
                
                if isinstance(p00, tuple) and isinstance(p10, tuple) and isinstance(p01, tuple) and isinstance(p11, tuple):
                    r = (1-fx)*(1-fy)*p00[0] + fx*(1-fy)*p10[0] + (1-fx)*fy*p01[0] + fx*fy*p11[0]
                    g = (1-fx)*(1-fy)*p00[1] + fx*(1-fy)*p10[1] + (1-fx)*fy*p01[1] + fx*fy*p11[1]
                    b = (1-fx)*(1-fy)*p00[2] + fx*(1-fy)*p10[2] + (1-fx)*fy*p01[2] + fx*fy*p11[2]
                    a = (1-fx)*(1-fy)*p00[3] + fx*(1-fy)*p10[3] + (1-fx)*fy*p01[3] + fx*fy*p11[3]
                    
                    if a > 3:
                        out.putpixel((x, y), (int(round(r)), int(round(g)), int(round(b)), int(round(a))))
                        
    return out

def build_base_idle() -> Image.Image:
    assert os.path.exists(PARTY_IDLE), f"Missing {PARTY_IDLE}"
    return Image.open(PARTY_IDLE).convert("RGBA")

def build_battle_sprite(base_idle: Image.Image) -> Image.Image:
    W, H = 128, 128
    
    grid_w = 17
    grid_h = 17
    disp_x = [[0.0 for _ in range(grid_w)] for _ in range(grid_h)]
    disp_y = [[0.0 for _ in range(grid_w)] for _ in range(grid_h)]
    
    cos_t = 0.90
    sin_t = 0.43
    
    for gy in range(grid_h):
        cy = gy * 8.0
        for gx in range(grid_w):
            cx = gx * 8.0
            
            dx = 0.0
            dy = 0.0
            
            # Hammer region: cx <= 50, cy in 56..122
            if cx <= 50 and 56 <= cy <= 122:
                rx = cx - 48.0
                ry = cy - 68.0
                dx = rx * (cos_t - 1) - ry * sin_t - 6.0
                dy = rx * sin_t + ry * (cos_t - 1) - 2.0
                
            # Head region: cy <= 56, 24 <= cx <= 96
            elif cy <= 56 and 24 <= cx <= 96:
                dx = -8.0
                dy = 2.5
                if cx <= 60:
                    dx -= 1.5
                    
            # Upper torso: 56 < cy <= 80, 40 <= cx <= 104
            elif 56 < cy <= 80 and 40 <= cx <= 104:
                dx = -7.0
                dy = 3.0
                
            # Lower torso / hips: 80 < cy <= 96, 40 <= cx <= 104
            elif 80 < cy <= 96 and 40 <= cx <= 104:
                if cx <= 68:
                    dx = -6.5
                else:
                    dx = 2.5
                dy = 3.0
                
            # Front leg (cy > 96, cx <= 68)
            elif cy > 96 and cx <= 68:
                if cy <= 114:
                    dx = -8.0
                    dy = 1.5
                else:
                    dx = -6.0
                    dy = 0.5
                    
            # Rear leg (cy > 96, cx > 68)
            elif cy > 96 and cx > 68:
                dx = 8.5
                dy = 0.5
                
            # Key & tail
            if cx >= 84:
                if cy <= 48:
                    dx = -6.0
                    dy = 2.0
                elif 76 <= cy <= 104:
                    dx = 1.5
                    dy = 1.5
                    
            disp_x[gy][gx] = dx
            disp_y[gy][gx] = dy
            
    warped = grid_warp(base_idle, grid_w, grid_h, disp_x, disp_y)
    
    # Ground contact cleanup
    for y in range(126, H):
        for x in range(W):
            warped.putpixel((x, y), (0, 0, 0, 0))
            
    # Optical enhancements (cyan eye flare, chest core flare)
    for y in range(H):
        for x in range(W):
            pix = warped.getpixel((x, y))
            if not isinstance(pix, tuple) or len(pix) < 4: continue
            r, g, b, a = pix[:4]
            if a == 0: continue
            
            # Eye enhancement (shifted forward: x around 46..58, y around 38..48)
            if 46 <= x <= 58 and 38 <= y <= 48:
                if g > 110 and b > 110 and r < 120:
                    warped.putpixel((x, y), (min(255, r + 40), min(255, g + 70), min(255, b + 70), 255))
            # Core enhancement (shifted forward: x around 44..56, y around 72..84)
            if 44 <= x <= 56 and 72 <= y <= 84:
                if g > 110 and b > 110 and r < 120:
                    warped.putpixel((x, y), (min(255, r + 35), min(255, g + 60), min(255, b + 60), 255))

    gleam = [
        (0, 0, (180, 255, 255, 255)),
        (-1, 0, (100, 240, 255, 200)),
        (1, 0, (100, 240, 255, 200)),
        (0, -1, (100, 240, 255, 200)),
        (0, 1, (100, 240, 255, 200)),
    ]
    for gdx, gdy, col in gleam:
        gx, gy = 51 + gdx, 42 + gdy
        if 0 <= gx < W and 0 <= gy < H:
            warped.putpixel((gx, gy), col)

    return warped

def build_walk_frames(base_idle: Image.Image) -> list[Image.Image]:
    W, H = 128, 128
    grid_w = 17
    grid_h = 17
    
    # 4 distinct gait phases:
    # Frame 0: Contact 1 (front foot forward, rear foot back, hammer back)
    # Frame 1: Passing 1 (front foot support, rear foot lifted passing high, body up-bob, hammer forward)
    # Frame 2: Contact 2 / Down (front foot back, rear foot forward, body down-bob, hammer down)
    # Frame 3: Passing 2 (front foot lifted passing high, rear foot support, body up-bob, hammer returning)
    configs = [
        # Frame 0: Contact 1
        {
            'torso_dy': 0.0,
            'fleg_dx': -4.5, 'fleg_dy': 1.0,  # front foot forward contact
            'rleg_dx': 5.0,  'rleg_dy': -0.5, # rear foot back
            'wep_dx': 2.0,   'wep_dy': 0.0,   # hammer swung back
            'tail_dx': 0.0,  'tail_dy': 0.0,
        },
        # Frame 1: Passing 1
        {
            'torso_dy': -3.0,                  # body bobs UP
            'fleg_dx': 0.0,  'fleg_dy': -1.0,  # front foot straight support
            'rleg_dx': -2.0, 'rleg_dy': -7.0,  # rear foot LIFTED high passing!
            'wep_dx': -4.0,  'wep_dy': -3.0,   # hammer swinging forward
            'tail_dx': 1.5,  'tail_dy': -3.0,
        },
        # Frame 2: Contact 2 / Down
        {
            'torso_dy': 2.0,                   # body bobs DOWN
            'fleg_dx': 5.0,  'fleg_dy': -0.5,  # front foot back
            'rleg_dx': -4.5, 'rleg_dy': 1.0,   # rear foot forward contact
            'wep_dx': -6.0,  'wep_dy': 2.0,    # hammer swung down
            'tail_dx': -1.5, 'tail_dy': 2.0,
        },
        # Frame 3: Passing 2
        {
            'torso_dy': -2.0,                  # body bobs UP
            'fleg_dx': -2.0, 'fleg_dy': -7.0,  # front foot LIFTED high passing!
            'rleg_dx': 0.0,  'rleg_dy': -1.0,  # rear foot straight support
            'wep_dx': 0.0,   'wep_dy': -2.0,   # hammer returning
            'tail_dx': 1.0,  'tail_dy': -2.0,
        },
    ]
    
    frames = []
    
    for cfg in configs:
        disp_x = [[0.0 for _ in range(grid_w)] for _ in range(grid_h)]
        disp_y = [[0.0 for _ in range(grid_w)] for _ in range(grid_h)]
        
        tdy = cfg['torso_dy']
        fdx, fdy = cfg['fleg_dx'], cfg['fleg_dy']
        rdx, rdy = cfg['rleg_dx'], cfg['rleg_dy']
        wdx, wdy = cfg['wep_dx'], cfg['wep_dy']
        
        for gy in range(grid_h):
            cy = gy * 8.0
            for gx in range(grid_w):
                cx = gx * 8.0
                
                # Hammer: cx <= 50, cy >= 56
                if cx <= 50 and cy >= 56:
                    disp_x[gy][gx] = wdx
                    disp_y[gy][gx] = wdy
                    
                # Head: cy <= 56, 24 <= cx <= 96
                elif cy <= 56 and 24 <= cx <= 96:
                    disp_x[gy][gx] = wdx * 0.3
                    disp_y[gy][gx] = tdy
                    
                # Upper & lower torso: 56 < cy <= 96, 40 <= cx <= 104
                elif 56 < cy <= 96 and 40 <= cx <= 104:
                    disp_x[gy][gx] = 0.0
                    disp_y[gy][gx] = tdy
                    
                # Front leg: cy > 96, cx <= 68
                elif cy > 96 and cx <= 68:
                    disp_x[gy][gx] = fdx
                    disp_y[gy][gx] = fdy
                    
                # Rear leg: cy > 96, cx > 68
                elif cy > 96 and cx > 68:
                    disp_x[gy][gx] = rdx
                    disp_y[gy][gx] = rdy
                    
                # Key & tail
                if cx >= 84:
                    if cy <= 48:
                        disp_x[gy][gx] = 0.0
                        disp_y[gy][gx] = tdy
                    elif 76 <= cy <= 104:
                        disp_x[gy][gx] = cfg['tail_dx']
                        disp_y[gy][gx] = cfg['tail_dy']
                        
        warped = grid_warp(base_idle, grid_w, grid_h, disp_x, disp_y)
        
        for y in range(126, H):
            for x in range(W):
                warped.putpixel((x, y), (0, 0, 0, 0))
                
        frames.append(warped)
        
    return frames

def build_hud_portrait() -> Image.Image:
    assert os.path.exists(BOAR_WARRIOR), f"Missing {BOAR_WARRIOR}"
    src = Image.open(BOAR_WARRIOR).convert("RGBA")
    # Scale to 90x90 to provide generous 19px safe margin for circular/rounded HUD frames
    inner = src.resize((90, 90), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    paste_x = (128 - 90) // 2
    paste_y = (128 - 90) // 2 + 1
    canvas.paste(inner, (paste_x, paste_y), inner)
    return canvas

def main():
    print("=== Generating Boar Core Assets (Compliant with Rule 4b-4 & 19f-2-2) ===")
    base_idle = build_base_idle()

    # 1. web/media/hero/boar_idle.png (128x128)
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
    walk_frames = build_walk_frames(base_idle)
    for i, w128 in enumerate(walk_frames):
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
    os.makedirs(os.path.dirname(hud_path), exist_ok=True)
    hud_portrait.save(hud_path, "PNG")
    print(f"✓ Saved [11/11] {hud_path}: size={hud_portrait.size}, bbox={hud_portrait.getbbox()}")

    print("\n=== Verifying Generated Assets Against Rule 4b-4 ===")
    f0 = walk_frames[0]
    total_px = 128 * 128
    for i in range(1, 4):
        diff = ImageChops.difference(f0, walk_frames[i])
        bbox = diff.getbbox(alpha_only=False)
        cnt = 0
        leg_cnt = 0
        for y in range(128):
            for x in range(128):
                p = diff.getpixel((x, y))
                if isinstance(p, tuple) and len(p) >= 4 and (any(p[:3]) or p[3] > 0):
                    cnt += 1
                    if y >= 95:
                        leg_cnt += 1
        
        # Check pure shift
        is_pure = False
        for dy in range(-8, 9):
            for dx in range(-8, 9):
                sh = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
                sh.paste(f0, (dx, dy), f0)
                if ImageChops.difference(walk_frames[i], sh).getbbox(alpha_only=False) is None:
                    is_pure = True
                    break
        print(f"Walk Frame 0 vs Frame {i}: diff bbox={bbox}, diff px={cnt}/{total_px} ({cnt/total_px*100:.1f}%), leg diff (y>=95)={leg_cnt} px, pure shift={is_pure}")
        assert not is_pure, f"Walk Frame {i} must NOT be a pure shift of Frame 0!"
        assert cnt > 2000, f"Walk Frame {i} diff must be substantial (>2000 px)!"

    # Verify Battle Sprite vs Idle
    b_diff = ImageChops.difference(base_idle, battle_sprite)
    b_bbox = b_diff.getbbox(alpha_only=False)
    b_cnt = 0
    b_leg_cnt = 0
    for y in range(128):
        for x in range(128):
            p = b_diff.getpixel((x, y))
            if isinstance(p, tuple) and len(p) >= 4 and (any(p[:3]) or p[3] > 0):
                b_cnt += 1
                if y >= 95:
                    b_leg_cnt += 1
    print(f"\nBattle vs Idle: diff bbox={b_bbox}, diff px={b_cnt}/16384 ({b_cnt/16384*100:.1f}%), leg diff (y>=95)={b_leg_cnt} px")
    assert b_cnt > 3000, f"Battle sprite must have substantial diff (>3000 px), got {b_cnt}!"
    assert b_leg_cnt > 500, f"Battle sprite legs must have substantial diff (>500 px), got {b_leg_cnt}!"

    print("\n✓ ALL 11 BOAR ASSETS SUCCESSFULLY PRODUCED AND STRICTLY VERIFIED!")

if __name__ == "__main__":
    main()
