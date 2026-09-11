#!/usr/bin/env python3
import sys
import os
import math
from typing import cast
from PIL import Image, ImageChops
from cc_helper import get_connected_components

# Import measure functions
sys.path.insert(0, os.path.dirname(__file__))
from verify_fox_action_poses import measure_staff_linearity, measure_shadow_rows

def test_hit():
    import test_arm_sleeve as tas
    hit_img = tas.hit_img
    idle_img = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/idle.png")
    battle_src = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/fox_battle.png")
    fox_idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/fox_idle.png") if os.path.exists("/opt/side/bravesoul-game/game/assets/sprites/player/fox_idle.png") else None
    
    print("=== 全面指標檢驗 ===")
    # 1. Connected components
    comps = get_connected_components(hit_img, alpha_thresh=40, y_max=118)
    print(f"1. 連通元件數 (alpha > 40, y < 118): {len(comps)}")
    assert len(comps) == 1, f"Expected 1 component, got {len(comps)}"
    
    # 2. Boundary clipping
    px = hit_img.load()
    assert px is not None
    x0_pixels = sum(1 for y in range(128) if cast(tuple[int,int,int,int], px[0, y])[3] > 0)
    x127_pixels = sum(1 for y in range(128) if cast(tuple[int,int,int,int], px[127, y])[3] > 0)
    y0_pixels = sum(1 for x in range(128) if cast(tuple[int,int,int,int], px[x, 0])[3] > 0)
    print(f"2. 邊界裁切檢查: x0={x0_pixels}, x127={x127_pixels}, y0={y0_pixels} (皆需為0)")
    assert x0_pixels == 0 and x127_pixels == 0 and y0_pixels == 0
    
    # 3. Diff vs idle
    diff = ImageChops.difference(idle_img, hit_img)
    diff_data = list(diff.convert("L").getdata())
    diff_px = sum(1 for x in diff_data if x > 10)
    print(f"3. 與 idle 差分像素數: {diff_px} px (門檻 >= 3000)")
    assert diff_px >= 3000
    
    # 4. Staff linearity
    resid = measure_staff_linearity(hit_img)
    print(f"4. 剛性法杖線性殘差: {resid:.2f} px")
    
    # 5. Shadow profile
    sh_rows = measure_shadow_rows(hit_img)
    print(f"5. 軟影數列 y118..127: {sh_rows}")
    assert sh_rows[0] > 40
    
    # 6. Weapon silhouette visibility ratio
    # Measure staff pixels outside body and on edge
    staff_px_total = 0
    staff_px_outside = 0
    staff_px_edge = 0
    
    b_px = tas.hit_body.load()
    s_px = tas.staff_hit.load()
    assert b_px is not None and s_px is not None
    
    for y in range(128):
        for x in range(128):
            sp = cast(tuple[int,int,int,int], s_px[x, y])
            if sp[3] > 40:
                staff_px_total += 1
                bp = cast(tuple[int,int,int,int], b_px[x, y])
                if bp[3] <= 40:
                    staff_px_outside += 1
                # Check if this pixel is on outer edge of hit_img
                # An edge pixel has at least one 8-neighbor with alpha <= 40
                is_edge = False
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 128 and 0 <= ny < 128:
                            if cast(tuple[int,int,int,int], px[nx, ny])[3] <= 40:
                                is_edge = True
                                break
                        else:
                            is_edge = True
                            break
                    if is_edge:
                        break
                if is_edge:
                    staff_px_edge += 1
                    
    edge_ratio = staff_px_edge / float(staff_px_total) * 100.0 if staff_px_total else 0.0
    outside_ratio = staff_px_outside / float(staff_px_total) * 100.0 if staff_px_total else 0.0
    print(f"6. 法杖剪影可見度: 邊緣可見比={edge_ratio:.1f}% ({staff_px_edge}/{staff_px_total} px), 體外剪影比={outside_ratio:.1f}% ({staff_px_outside}/{staff_px_total} px)")
    assert edge_ratio >= 10.0, f"Edge ratio {edge_ratio:.1f}% < 10.0%!"

    # 7. Check diff vs battle_src
    diff_battle = ImageChops.difference(battle_src, hit_img)
    diff_b_px = sum(1 for x in list(diff_battle.convert("L").getdata()) if x > 10)
    print(f"7. 與 fox_battle 差分像素數: {diff_b_px} px (不可為 0 / 假姿態)")
    assert diff_b_px > 3000

if __name__ == "__main__":
    test_hit()
