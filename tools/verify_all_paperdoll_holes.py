import os
from PIL import Image
from collections import deque

BASE = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll"

def count_holes(im, conn=4, threshold=1):
    w, h = im.size
    visited = [[False]*w for _ in range(h)]
    q = deque()
    
    for x in range(w):
        for y in [0, h - 1]:
            p = im.getpixel((x, y))
            if p[3] < threshold and not visited[y][x]:
                visited[y][x] = True
                q.append((x, y))
    for y in range(h):
        for x in [0, w - 1]:
            p = im.getpixel((x, y))
            if p[3] < threshold and not visited[y][x]:
                visited[y][x] = True
                q.append((x, y))
                
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if conn == 8:
        dirs += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
    while q:
        cx, cy = q.popleft()
        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h:
                if not visited[ny][nx] and im.getpixel((nx, ny))[3] < threshold:
                    visited[ny][nx] = True
                    q.append((nx, ny))
                    
    holes = []
    for y in range(h):
        for x in range(w):
            if im.getpixel((x, y))[3] < threshold and not visited[y][x]:
                holes.append((x, y))
    return holes

races = ["rabbit", "lion", "fox", "boar", "macaque"]

print("================================================================")
print("1. 五族 × chassis 單層 flood-fill 破洞統計 (Rule 4c-6)")
print("================================================================")
for race in races:
    cdir = f"{BASE}/{race}/chassis"
    for fn in sorted(os.listdir(cdir)):
        if fn.endswith(".png"):
            p = f"{cdir}/{fn}"
            im = Image.open(p).convert("RGBA")
            h4 = count_holes(im, conn=4, threshold=1)
            h8 = count_holes(im, conn=8, threshold=1)
            print(f"  {race:10} chassis/{fn:22} -> 4conn: {len(h4):2d} px | 8conn: {len(h8):2d} px")

print("\n================================================================")
print("2. 五族 × (裸素體 + 每一套 costume) 全套合成破洞統計")
print("================================================================")

# Default equipment for each race (excluding costume and chassis)
# Slot order: winding_key(5) -> back_curio(8) -> chassis(10) -> head_unit(20) -> costume(25) -> optic_core(30) -> weapon(40)
defaults = {
    "rabbit": {
        "winding_key": "key_classic_brass.png",
        "back_curio": "curio_clockwork_pigeon.png",
        "head_unit": "ear_rabbit_straight.png",
        "optic_core": "core_cyan_emerald.png",
        "weapon": "wpn_dawn_blade.png",
    },
    "lion": {
        "winding_key": "key_classic_brass.png",
        "back_curio": "curio_lion_fan_tail.png",
        "head_unit": "ear_lion_gilded_mane.png",
        "optic_core": "core_amber_sun.png",
        "weapon": "wpn_knight_lance.png",
    },
    "fox": {
        "winding_key": "key_classic_brass.png",
        "back_curio": "curio_fox_astral_tail.png",
        "head_unit": "ear_fox_radar.png",
        "optic_core": "core_cyan_emerald.png",
        "weapon": "wpn_astral_staff.png",
    },
    "boar": {
        "winding_key": "key_classic_brass.png",
        "back_curio": "curio_spring_tail.png",
        "head_unit": "ear_boar_rivet_cowl.png",
        "optic_core": "core_cyan_emerald.png",
        "weapon": "wpn_anvil_greathammer.png",
    },
    "macaque": {
        "winding_key": "key_classic_brass.png",
        "back_curio": "curio_spring_tail.png",
        "head_unit": "ear_macaque_coaxial.png",
        "optic_core": "core_cyan_emerald.png",
        "weapon": "wpn_spring_claws.png",
    },
}

for race in races:
    rdir = f"{BASE}/{race}"
    eq = defaults[race]
    chassis_list = sorted([fn for fn in os.listdir(f"{rdir}/chassis") if fn.endswith(".png")])
    costume_list = ["(bare)"] + sorted([fn for fn in os.listdir(f"{rdir}/costume") if fn.endswith(".png")])
    
    for ch in chassis_list:
        for cos in costume_list:
            comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            # winding_key
            comp = Image.alpha_composite(comp, Image.open(f"{rdir}/winding_key/{eq['winding_key']}").convert("RGBA"))
            # back_curio
            comp = Image.alpha_composite(comp, Image.open(f"{rdir}/back_curio/{eq['back_curio']}").convert("RGBA"))
            # chassis
            comp = Image.alpha_composite(comp, Image.open(f"{rdir}/chassis/{ch}").convert("RGBA"))
            # head_unit
            comp = Image.alpha_composite(comp, Image.open(f"{rdir}/head_unit/{eq['head_unit']}").convert("RGBA"))
            # costume (if not bare)
            if cos != "(bare)":
                comp = Image.alpha_composite(comp, Image.open(f"{rdir}/costume/{cos}").convert("RGBA"))
            # optic_core
            comp = Image.alpha_composite(comp, Image.open(f"{rdir}/optic_core/{eq['optic_core']}").convert("RGBA"))
            # weapon
            comp = Image.alpha_composite(comp, Image.open(f"{rdir}/weapon/{eq['weapon']}").convert("RGBA"))
            
            h4 = count_holes(comp, conn=4, threshold=1)
            h8 = count_holes(comp, conn=8, threshold=1)
            print(f"  {race:8} | chassis: {ch:20} | costume: {cos:26} -> 4conn: {len(h4):2d} px | 8conn: {len(h8):2d} px")
