#!/usr/bin/env python3
"""
生成熾火赤狐 MaplePaperdoll 骨骼錨點緊湊切片與素材資產
依據楓之谷 Character.wz 骨骼錨點架構與 MaplePaperdoll 組件
"""
import os
import numpy as np
from PIL import Image, ImageDraw

REPO_ROOT = '/opt/side/bravesoul-game'
PARTS_DIR = f'{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/maple_parts'

for sub in ['body', 'head_unit', 'eyes', 'costume', 'weapon', 'winding_key']:
    os.makedirs(f'{PARTS_DIR}/{sub}', exist_ok=True)

# 載入 512 原始無頭/全素體參照
orange_ch = Image.open('/tmp/old_fox_chassis.png').convert('RGBA')
ivory_ch = Image.open('/tmp/old_fox_ivory.png').convert('RGBA')
emerald_ch = Image.open('/tmp/old_fox_emerald.png').convert('RGBA')

# -------------------------------------------------------------
# 1. 背部發條鑰匙 (key_classic_brass.png)
# -------------------------------------------------------------
fox_key_img = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
for y in range(225, 332):
    for x in range(370, 431):
        p = orange_ch.getpixel((x, y))
        if p[3] > 0:
            fox_key_img.putpixel((x, y), p)

key_crop = fox_key_img.crop((370, 225, 431, 332)) # 61 x 107
key_crop.save(f'{PARTS_DIR}/winding_key/key_classic_brass.png')
print("Saved key_classic_brass.png:", key_crop.size)

# -------------------------------------------------------------
# 2. 狐耳頭部單元 (ear_fox_radar_*.png)
# -------------------------------------------------------------
def extract_ears(ch):
    ear_canvas = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
    for y in range(43, 150):
        for x in range(139, 394):
            p = ch.getpixel((x, y))
            if p[3] > 0:
                ear_canvas.putpixel((x, y), p)
    return ear_canvas.crop((140, 43, 393, 149)) # 253 x 106

ear_orange = extract_ears(orange_ch)
ear_ivory = extract_ears(ivory_ch)
ear_emerald = extract_ears(emerald_ch)

ear_orange.save(f'{PARTS_DIR}/head_unit/ear_fox_radar_orange.png')
ear_ivory.save(f'{PARTS_DIR}/head_unit/ear_fox_radar_ivory.png')
ear_emerald.save(f'{PARTS_DIR}/head_unit/ear_fox_radar_emerald.png')
print("Saved ear_fox_radar_*.png:", ear_orange.size)

# -------------------------------------------------------------
# 3. 光學義眼 (eyes_cyan_emerald, eyes_amber_gold, eyes_blink)
# -------------------------------------------------------------
w_eye, h_eye = 165, 60
e_cyan = Image.new('RGBA', (w_eye, h_eye), (0, 0, 0, 0))
e_amber = Image.new('RGBA', (w_eye, h_eye), (0, 0, 0, 0))
e_blink = Image.new('RGBA', (w_eye, h_eye), (0, 0, 0, 0))

draw_c = ImageDraw.Draw(e_cyan)
draw_a = ImageDraw.Draw(e_amber)
draw_b = ImageDraw.Draw(e_blink)

col_outline = (30, 20, 15, 255)
col_pupil = (15, 12, 10, 255)
col_white = (255, 255, 255, 255)

# Cyan
c_top = (12, 85, 95, 255)
c_mid = (25, 180, 185, 255)
c_bot = (50, 235, 225, 255)

# Amber
a_top = (120, 55, 10, 255)
a_mid = (220, 135, 15, 255)
a_bot = (255, 205, 40, 255)

for cx, cy in [(36.5, 32.0), (134.5, 32.0)]:
    # Cyan
    draw_c.ellipse([cx - 17.5, cy - 20, cx + 17.5, cy + 20], fill=col_outline)
    draw_c.ellipse([cx - 15.5, cy - 18, cx + 15.5, cy + 18], fill=c_top)
    draw_c.ellipse([cx - 14.5, cy - 14, cx + 14.5, cy + 17], fill=c_mid)
    draw_c.ellipse([cx - 12.5, cy - 6, cx + 12.5, cy + 16], fill=c_bot)
    draw_c.ellipse([cx - 9.5, cy - 15, cx + 9.5, cy + 11], fill=col_pupil)
    draw_c.ellipse([cx - 7.5, cy - 12, cx - 1.5, cy - 6], fill=col_white)
    draw_c.ellipse([cx + 2.5, cy + 2, cx + 6.5, cy + 6], fill=col_white)
    flick_dir = -1 if cx < 80 else 1
    draw_c.line([cx + 14.5*flick_dir, cy - 14, cx + 19.5*flick_dir, cy - 18], fill=col_outline, width=2)

    # Amber
    draw_a.ellipse([cx - 17.5, cy - 20, cx + 17.5, cy + 20], fill=col_outline)
    draw_a.ellipse([cx - 15.5, cy - 18, cx + 15.5, cy + 18], fill=a_top)
    draw_a.ellipse([cx - 14.5, cy - 14, cx + 14.5, cy + 17], fill=a_mid)
    draw_a.ellipse([cx - 12.5, cy - 6, cx + 12.5, cy + 16], fill=a_bot)
    draw_a.ellipse([cx - 9.5, cy - 15, cx + 9.5, cy + 11], fill=col_pupil)
    draw_a.ellipse([cx - 7.5, cy - 12, cx - 1.5, cy - 6], fill=col_white)
    draw_a.ellipse([cx + 2.5, cy + 2, cx + 6.5, cy + 6], fill=col_white)
    draw_a.line([cx + 14.5*flick_dir, cy - 14, cx + 19.5*flick_dir, cy - 18], fill=col_outline, width=2)

    # Blink
    draw_b.arc([cx - 16, cy - 8, cx + 16, cy + 10], start=200, end=340, fill=col_outline, width=4)
    draw_b.line([cx + 14*flick_dir, cy + 2, cx + 18*flick_dir, cy - 2], fill=col_outline, width=2)

e_cyan.save(f'{PARTS_DIR}/eyes/eyes_cyan_emerald.png')
e_amber.save(f'{PARTS_DIR}/eyes/eyes_amber_gold.png')
e_blink.save(f'{PARTS_DIR}/eyes/eyes_blink.png')
print("Saved eyes_*.png: 165x60")

# -------------------------------------------------------------
# 4. 素體塗裝 (paint_*.png, 512x512)
# -------------------------------------------------------------
def make_clean_body(ch):
    body = ch.copy()
    col_l = ch.getpixel((175, 195))
    col_r = ch.getpixel((355, 195))
    
    # 覆蓋眼窩為純淨面甲底色 (left peach, right cream)
    for gy in range(170, 225):
        for gx in range(190, 340):
            dl = (((gx - 216.5)/19.5)**2 + ((gy - 197.0)/22.0)**2)**0.5
            dr = (((gx - 314.5)/19.5)**2 + ((gy - 197.0)/22.0)**2)**0.5
            if dl <= 1.0:
                body.putpixel((gx, gy), col_l)
            elif dr <= 1.0:
                body.putpixel((gx, gy), col_r)
                
    # 移除上方耳朵 (y < 144)
    for y in range(40, 144):
        for x in range(130, 400):
            body.putpixel((x, y), (0, 0, 0, 0))
            
    # 精確減除背部發條鑰匙外露區域 (y < 312, x in [370, 435])
    for y in range(225, 312):
        for x in range(370, 431):
            ky = y - 225
            kx = x - 370
            if 0 <= kx < key_crop.size[0] and 0 <= ky < key_crop.size[1]:
                if key_crop.getpixel((kx, ky))[3] > 0:
                    body.putpixel((x, y), (0, 0, 0, 0))
                    
    return body

body_orange = make_clean_body(orange_ch)
body_ivory = make_clean_body(ivory_ch)
body_emerald = make_clean_body(emerald_ch)

body_orange.save(f'{PARTS_DIR}/body/paint_fox_orange.png')
body_ivory.save(f'{PARTS_DIR}/body/paint_ivory_stock.png')
body_emerald.save(f'{PARTS_DIR}/body/paint_emerald_glaze.png')
print("Saved paint_*.png: 512x512")

# -------------------------------------------------------------
# 5. 外裝 (costume_astral_cape, costume_astral_observer)
# -------------------------------------------------------------
cape_512 = Image.open(f'{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/costume/costume_astral_cape_512.png').convert('RGBA')
c_arr = np.array(cape_512)
for y in range(295, 380):
    for x in range(235, 278):
        c_arr[y, x] = [0, 0, 0, 0]
is_outline = (c_arr[:, :, 0] < 50) & (c_arr[:, :, 1] < 50) & (c_arr[:, :, 2] < 70) & (c_arr[:, :, 3] > 40)
c_arr[is_outline, 3] = 255
c_arr[c_arr[:, :, 3] < 90] = [0, 0, 0, 0]
cape_clean = Image.fromarray(c_arr, 'RGBA').crop((174, 262, 345, 430)) # 171 x 168
cape_clean.save(f'{PARTS_DIR}/costume/costume_astral_cape.png')

obs_512 = Image.open(f'{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/costume/costume_astral_observer_512.png').convert('RGBA')
o_arr = np.array(obs_512)
for y in range(215, 256):
    for x in range(139, 362):
        o_arr[y, x] = [0, 0, 0, 0]
for y in range(326, 351):
    for x in range(139, 154):
        o_arr[y, x] = [0, 0, 0, 0]
for y in range(331, 351):
    for x in range(344, 362):
        o_arr[y, x] = [0, 0, 0, 0]
o_arr[o_arr[:, :, 3] < 35] = [0, 0, 0, 0]
obs_clean = Image.fromarray(o_arr, 'RGBA').crop((139, 256, 361, 445)) # 222 x 189
obs_clean.save(f'{PARTS_DIR}/costume/costume_astral_observer.png')
print("Saved costume_*.png: cape=171x168, observer=222x189")

# -------------------------------------------------------------
# 6. 武器 (wpn_astral_staff)
# -------------------------------------------------------------
wpn_512 = Image.open(f'{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff_512.png').convert('RGBA')
w_crop = wpn_512.crop((327, 148, 441, 505)) # 114 x 357
w_w, w_h = w_crop.size
for y in range(w_h):
    for x in range(w_w):
        if y < 125 and x < 42:
            w_crop.putpixel((x, y), (0, 0, 0, 0))
        if y > 235 and x < 38:
            w_crop.putpixel((x, y), (0, 0, 0, 0))
w_crop.save(f'{PARTS_DIR}/weapon/wpn_astral_staff.png')
print("Saved wpn_astral_staff.png: 114x357")
