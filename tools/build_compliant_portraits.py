#!/usr/bin/env python3
"""
tools/build_compliant_portraits.py
通用首領與角色半身像/頭像標準化生成工具：
- 剔除純白邊緣外框與白底，維持邊緣平滑
- 鋪設標準深色底板 PORTRAIT_BG (65, 45, 56, 255)
- 生成符合規範的 384x480 對話半身像與比對檢驗圖
"""
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from collections import deque

PORTRAIT_BG = (65, 45, 56, 255)
ROOT = "/opt/side/bravesoul-game"
REPO_PORTRAITS = os.path.join(ROOT, "game/assets/sprites/portraits")
PROOFS_DIR = os.path.join(ROOT, "proofs/enemy_audit")
BACKUP_DIR = "/tmp/old_portraits"

os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(PROOFS_DIR, exist_ok=True)

def remove_pure_white_bg(im, threshold=238):
    im = im.convert("RGBA")
    w, h = im.size
    arr = np.array(im)
    is_white = (arr[:, :, 0] > threshold) & (arr[:, :, 1] > threshold) & (arr[:, :, 2] > threshold)
    visited = np.zeros((h, w), dtype=bool)
    bg_mask = np.zeros((h, w), dtype=bool)
    
    q = deque()
    for x in range(w):
        if is_white[0, x]:
            q.append((0, x)); visited[0, x] = True
        if is_white[h-1, x]:
            q.append((h-1, x)); visited[h-1, x] = True
    for y in range(h):
        if is_white[y, 0] and not visited[y, 0]:
            q.append((y, 0)); visited[y, 0] = True
        if is_white[y, w-1] and not visited[y, w-1]:
            q.append((y, w-1)); visited[y, w-1] = True
            
    while q:
        cy, cx = q.popleft()
        bg_mask[cy, cx] = True
        for dy, dx in ((-1,0), (1,0), (0,-1), (0,1)):
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                visited[ny, nx] = True
                if is_white[ny, nx]:
                    q.append((ny, nx))
                    
    arr[:, :, 3] = (~bg_mask).astype(np.uint8) * 255
    return Image.fromarray(arr)

# ==========================================
# 1. PROCESS FOG_HIDE (霧隱)
# ==========================================
print("Processing fog_hide...")
old_fog_hide_path = os.path.join(REPO_PORTRAITS, "fog_hide.png")
if os.path.exists(old_fog_hide_path):
    Image.open(old_fog_hide_path).save(os.path.join(BACKUP_DIR, "fog_hide.png"))

raw_fog = Image.open("/tmp/fog_hide_raw.png")
cut_fog = remove_pure_white_bg(raw_fog, threshold=235)
bbox_fog = cut_fog.getbbox()
if bbox_fog is None:
    raise ValueError("No bbox for fog_hide")
crop_fog = cut_fog.crop(bbox_fog)

scale_fog = min(350 / crop_fog.width, 430 / crop_fog.height)
w_fog = int(crop_fog.width * scale_fog)
h_fog = int(crop_fog.height * scale_fog)
res_fog = crop_fog.resize((w_fog, h_fog), Image.Resampling.LANCZOS)

canvas_fog = Image.new("RGBA", (384, 480), PORTRAIT_BG)
x_fog = (384 - w_fog) // 2
y_fog = 480 - h_fog - 15
canvas_fog.paste(res_fog, (x_fog, y_fog), res_fog)

dest_fog_hide = os.path.join(REPO_PORTRAITS, "fog_hide.png")
canvas_fog.save(dest_fog_hide, "PNG")
print(f"Saved {dest_fog_hide}")

# Head crop for fog_hide:
# In canvas_fog, character head is located roughly at:
# x: center (80, 304), y: (30, 254)
head_box_fog = (80, 35, 304, 259)
head_fog = canvas_fog.crop(head_box_fog).resize((488, 488), Image.Resampling.NEAREST)
head_fog_path = os.path.join(PROOFS_DIR, "fog_hide_portrait_head_crop.png")
head_fog.save(head_fog_path, "PNG")
print(f"Saved {head_fog_path}")

# Compare panel for fog_hide:
old_fog_im = Image.open(os.path.join(BACKUP_DIR, "fog_hide.png"))
panel_fog = Image.new("RGB", (800, 540), (24, 20, 28))
draw_fog = ImageDraw.Draw(panel_fog)
panel_fog.paste(old_fog_im.convert("RGB").resize((384, 480), Image.Resampling.LANCZOS), (12, 40))
panel_fog.paste(canvas_fog.convert("RGB"), (404, 40))
draw_fog.text((20, 12), "BEFORE (Old 2026-08-31 Furry Fox - VIOLATION)", fill=(230, 80, 80))
draw_fog.text((420, 12), "AFTER (New Clockwork Grey Fox Ninja - COMPLIANT)", fill=(80, 230, 120))
compare_fog_path = os.path.join(PROOFS_DIR, "fog_hide_portrait_compare.png")
panel_fog.save(compare_fog_path, "PNG")
print(f"Saved {compare_fog_path}")

# ==========================================
# 2. PROCESS BOAR (石拳 / 鋼牙豕)
# ==========================================
print("Processing boar...")
old_boar_path = os.path.join(REPO_PORTRAITS, "boar.png")
if os.path.exists(old_boar_path):
    Image.open(old_boar_path).save(os.path.join(BACKUP_DIR, "boar.png"))

raw_boar = Image.open("/tmp/boar_highres_raw.png")
cut_boar = remove_pure_white_bg(raw_boar, threshold=238)
bbox_boar = cut_boar.getbbox()
if bbox_boar is None:
    raise ValueError("No bbox for boar")

# Crop from top of horns down to waist
crop_boar = cut_boar.crop((bbox_boar[0], bbox_boar[1], bbox_boar[2], min(cut_boar.height, bbox_boar[1] + 740)))
w_b, h_b = crop_boar.size

scale_boar = min(355 / w_b, 430 / h_b)
new_w_b = int(w_b * scale_boar)
new_h_b = int(h_b * scale_boar)
resized_boar = crop_boar.resize((new_w_b, new_h_b), Image.Resampling.LANCZOS)

canvas_boar = Image.new("RGBA", (384, 480), PORTRAIT_BG)
paste_x_b = (384 - new_w_b) // 2
paste_y_b = (480 - new_h_b) // 2 + 5
canvas_boar.paste(resized_boar, (paste_x_b, paste_y_b), resized_boar)

dest_boar = os.path.join(REPO_PORTRAITS, "boar.png")
canvas_boar.save(dest_boar, "PNG")
print(f"Saved {dest_boar}")

# Head crop for boar:
# Head, crest horns, tusks, and winding key:
head_box_boar = (80, 35, 304, 259)
head_boar = canvas_boar.crop(head_box_boar).resize((488, 488), Image.Resampling.NEAREST)
head_boar_path = os.path.join(PROOFS_DIR, "boar_portrait_head_crop.png")
head_boar.save(head_boar_path, "PNG")
print(f"Saved {head_boar_path}")

# Compare panel for boar:
old_boar_im = Image.open(os.path.join(BACKUP_DIR, "boar.png"))
panel_boar = Image.new("RGB", (800, 540), (24, 20, 28))
draw_boar = ImageDraw.Draw(panel_boar)
# Old boar was 128x128, upscale cleanly
panel_boar.paste(old_boar_im.convert("RGB").resize((384, 480), Image.Resampling.NEAREST), (12, 40))
panel_boar.paste(canvas_boar.convert("RGB"), (404, 40))
draw_boar.text((20, 12), "BEFORE (Old 128x128 Low-Res Placeholder - SPEC MISMATCH)", fill=(230, 80, 80))
draw_boar.text((420, 12), "AFTER (New 384x480 High-Res Clockwork Boar - COMPLIANT)", fill=(80, 230, 120))
compare_boar_path = os.path.join(PROOFS_DIR, "boar_portrait_compare.png")
panel_boar.save(compare_boar_path, "PNG")
print(f"Saved {compare_boar_path}")

print("COMPLIANT PORTRAITS BUILD FINISHED SUCCESSFULLY.")
