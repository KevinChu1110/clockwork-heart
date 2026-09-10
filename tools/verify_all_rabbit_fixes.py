import os
import math
from PIL import Image
from collections import deque

repo = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
r_dir = f"{repo}/game/assets/sprites/player/paperdoll/rabbit"
w, h = 128, 128

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

print("=== 1. Checking wpn_dawn_blade.png Statistics ===")
wpn = Image.open(f"{r_dir}/weapon/wpn_dawn_blade.png").convert("RGBA")
bbox = wpn.getbbox()
print(f"Bbox: {bbox}")

solid = 0
semi = 0
zero = 0
for y in range(h):
    for x in range(w):
        a = wpn.getpixel((x, y))[3]
        if a == 255: solid += 1
        elif a > 0: semi += 1
        else: zero += 1

print(f"Solid pixels: {solid}")
print(f"Semi-transparent pixels: {semi} ({semi/(solid+semi)*100:.1f}%)")

# Transparent pixels inside rows of the weapon:
row_holes = []
for y in range(bbox[1], bbox[3]):
    xs = [x for x in range(bbox[0], bbox[2]) if wpn.getpixel((x, y))[3] == 255]
    if len(xs) >= 2:
        for x in range(min(xs), max(xs) + 1):
            if wpn.getpixel((x, y))[3] == 0:
                row_holes.append((x, y))

print(f"Transparent row holes inside weapon: {len(row_holes)} (Old baseline: 13, Failed attempt: 61)")

print("\n=== 2. Checking chassis single-layer flood-fill holes ===")
for p_name in ["paint_ivory_stock.png", "paint_brass_gold.png", "paint_midnight_navy.png"]:
    ch = Image.open(f"{r_dir}/chassis/{p_name}").convert("RGBA")
    h4 = count_holes(ch, conn=4)
    print(f"  {p_name:24} -> 4conn holes: {len(h4)} px")

print("\n=== 3. Checking 12 composite variants (3 chassis × 4 costumes) ===")
key = Image.open(f"{r_dir}/winding_key/key_classic_brass.png").convert("RGBA")
pigeon = Image.open(f"{r_dir}/back_curio/curio_clockwork_pigeon.png").convert("RGBA")
head = Image.open(f"{r_dir}/head_unit/ear_rabbit_straight.png").convert("RGBA")
core = Image.open(f"{r_dir}/optic_core/core_cyan_emerald.png").convert("RGBA")

# Base baseline (ivory + nutcracker without weapon)
base_no_wpn = Image.new("RGBA", (w, h), (0, 0, 0, 0))
base_no_wpn.alpha_composite(key)
base_no_wpn.alpha_composite(pigeon)
base_no_wpn.alpha_composite(Image.open(f"{r_dir}/chassis/paint_ivory_stock.png").convert("RGBA"))
base_no_wpn.alpha_composite(head)
base_no_wpn.alpha_composite(Image.open(f"{r_dir}/costume/costume_nutcracker_guard.png").convert("RGBA"))
base_no_wpn.alpha_composite(core)
base_holes = count_holes(base_no_wpn, conn=4)
print(f"Base without weapon holes count: {len(base_holes)} px")

chassis_list = sorted([fn for fn in os.listdir(f"{r_dir}/chassis") if fn.endswith(".png")])
costume_list = ["(bare)"] + sorted([fn for fn in os.listdir(f"{r_dir}/costume") if fn.endswith(".png")])

for ch in chassis_list:
    ch_im = Image.open(f"{r_dir}/chassis/{ch}").convert("RGBA")
    for cos in costume_list:
        comp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        comp.alpha_composite(key)
        comp.alpha_composite(pigeon)
        comp.alpha_composite(ch_im)
        comp.alpha_composite(head)
        if cos != "(bare)":
            cos_im = Image.open(f"{r_dir}/costume/{cos}").convert("RGBA")
            comp.alpha_composite(cos_im)
        comp.alpha_composite(core)
        comp.alpha_composite(wpn)
        
        h4 = count_holes(comp, conn=4)
        h8 = count_holes(comp, conn=8)
        new_holes = set(h4) - set(base_holes)
        print(f"  {ch:22} | {cos:26} -> 4conn: {len(h4):2d} px (new={len(new_holes)}) | 8conn: {len(h8):2d} px")

print("\n=== 4. Generating Visual Evidence Proofs ===")
# A. Single layer weapon on bright magenta (255, 0, 255)
mag_wpn = Image.new("RGBA", (w, h), (255, 0, 255, 255))
mag_wpn.alpha_composite(wpn)
mag_wpn.save(f"{repo}/screenshots/proof_weapon_on_magenta.png")
crop_w = mag_wpn.crop((25, 80, 95, 128))
zoom_w = crop_w.resize((crop_w.width * 4, crop_w.height * 4), Image.Resampling.NEAREST if hasattr(Image, "Resampling") else 0)
zoom_w.save(f"{repo}/screenshots/proof_weapon_on_magenta_zoom.png")
print("  ✓ proof_weapon_on_magenta_zoom.png saved.")

# B. Full standard composite on magenta and transparent
comp_std = Image.open(f"{r_dir}/proof_paperdoll_rabbit_composite.png")
zoom_comp = comp_std.resize((comp_std.width * 4, comp_std.height * 4), Image.Resampling.NEAREST if hasattr(Image, "Resampling") else 0)
zoom_comp.save(f"{repo}/screenshots/proof_rabbit_composite_zoom.png")

crop_hilt = comp_std.crop((25, 80, 60, 105))
zoom_hilt = crop_hilt.resize((crop_hilt.width * 4, crop_hilt.height * 4), Image.Resampling.NEAREST if hasattr(Image, "Resampling") else 0)
zoom_hilt.save(f"{repo}/screenshots/proof_rabbit_hilt_zoom.png")
print("  ✓ proof_rabbit_hilt_zoom.png saved.")
print("  ✓ proof_rabbit_composite_zoom.png saved.")
