#!/usr/bin/env python3
"""
生成熾火赤狐 MaplePaperdoll 骨骼錨點緊湊切片與素材資產 (精修版)
依據 sideqa 審查意見修復：
1. 素體面甲去眼處平滑精修、消除色塊補丁邊界、清除雙側眼下與額頭黑線雜訊碎片
2. 外裝 costume_astral_observer 開出心臟核心視窗 (0-ART51)，修除肩膀懸空直角雜邊
3. 武器法杖 wpn_astral_staff 去除手柄交界處深褐色遮罩雜點與半透明噪點
"""
import os
import json
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label

REPO_ROOT = '/opt/side/bravesoul-game'
PARTS_DIR = f'{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/maple_parts'
SPEC_JSON_PATH = f'{REPO_ROOT}/game/data/tables/maple_paperdoll_fox.json'

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
# 4. 素體塗裝 (paint_*.png, 512x512) - 精修去眼去雜訊
# -------------------------------------------------------------
def make_clean_body_refined(ch):
    body = ch.copy()
    col_l = ch.getpixel((180, 195))
    col_r = ch.getpixel((340, 195))
    
    # 1. 左眼及左眼上方眉線、眼窩平滑補齊底色 (x in 190..235, y in 148..225)
    for y in range(148, 226):
        for x in range(190, 236):
            body.putpixel((x, y), col_l)
            
    # 左側眼下/鼻側殘留折線雜訊碎片 (x in 240..248, y in 228..235)
    for y in range(228, 236):
        for x in range(240, 248):
            body.putpixel((x, y), col_l if x <= 235 else col_r)
            
    # 左臉頰邊緣下緣毛邊修正 (x in 180..205, y in 238..248)
    for y in range(238, 249):
        for x in range(180, 206):
            p = body.getpixel((x, y))
            if p[3] > 50 and p[0] > 235 and p[1] > 195:
                body.putpixel((x, y), col_l)

    # 2. 右眼及右眼上方眉線、眼窩平滑補齊底色 (x in 285..342, y in 148..225)
    for y in range(148, 168):
        for x in range(300, 335):
            body.putpixel((x, y), col_r)
            
    for y in range(168, 226):
        for x in range(285, 342):
            body.putpixel((x, y), col_r)
            
    # 右眼下方與鼻子右側嘴唇上方殘留折線與三角形雜訊碎片 (x in 283..294, y in 228..236)
    for y in range(228, 236):
        for x in range(283, 294):
            body.putpixel((x, y), col_r)
            
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

body_orange = make_clean_body_refined(orange_ch)
body_ivory = make_clean_body_refined(ivory_ch)
body_emerald = make_clean_body_refined(emerald_ch)

body_orange.save(f'{PARTS_DIR}/body/paint_fox_orange.png')
body_ivory.save(f'{PARTS_DIR}/body/paint_ivory_stock.png')
body_emerald.save(f'{PARTS_DIR}/body/paint_emerald_glaze.png')
print("Saved paint_*.png (refined): 512x512")

# -------------------------------------------------------------
# 5. 外裝 (costume_astral_cape, costume_astral_observer)
# -------------------------------------------------------------
# 5.1 costume_astral_cape
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

# 5.2 costume_astral_observer (精修版：心臟視窗 + 肩膀貼合輪廓)
obs_512 = Image.open(f'{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/costume/costume_astral_observer_512.png').convert('RGBA')
o_arr = np.array(obs_512)

# 清除背景雜訊
o_arr[o_arr[:, :, 3] < 50] = [0, 0, 0, 0]

# 下擺對齊裙甲平整 (y=422)
o_arr[422:, :] = [0, 0, 0, 0]

# 頸部上方歸零 (y < 266)
o_arr[:266, :] = [0, 0, 0, 0]

# 順著胸腹軀幹輪廓平滑過渡 (x in [179, 305] 保持軀幹平整無多餘突出邊界)
for y in range(266, 346):
    for x in range(0, 179):
        o_arr[y, x] = [0, 0, 0, 0]
    for x in range(305, 512):
        o_arr[y, x] = [0, 0, 0, 0]

for y in range(346, 422):
    for x in range(0, 167):
        o_arr[y, x] = [0, 0, 0, 0]
    for x in range(316, 512):
        o_arr[y, x] = [0, 0, 0, 0]

# 開出心臟核心視窗 (0-ART51)
# 身體發光核心位於 x in [245, 282], y in [303, 335]，中心 (264.5, 318.5)
for y in range(295, 345):
    for x in range(238, 290):
        d = (((x - 264.5) / 20.0) ** 2 + ((y - 318.5) / 18.0) ** 2) ** 0.5
        if d <= 1.0:
            o_arr[y, x] = [0, 0, 0, 0]
        elif d <= 1.2:
            # 圓弧外圈帶有立體金邊過渡
            rim_col = [225, 180, 55, 255]
            alpha_blend = (1.2 - d) / 0.2
            orig = o_arr[y, x]
            if orig[3] > 0:
                new_rgb = [int(orig[i] * (1 - alpha_blend) + rim_col[i] * alpha_blend) for i in range(3)]
                o_arr[y, x] = [new_rgb[0], new_rgb[1], new_rgb[2], 255]

# 將視窗上方多餘的小青綠寶石徽記轉為金色鉚釘 (x in 235..250, y in 290..306)，確保胸口青綠核心唯一且純粹
for y in range(290, 306):
    for x in range(235, 250):
        if o_arr[y, x, 3] > 0 and o_arr[y, x, 1] > 140 and o_arr[y, x, 2] > 120 and o_arr[y, x, 0] < 120:
            o_arr[y, x, :3] = [215, 165, 50]

# 取得非透明像素範圍並裁切緊湊 Sprite
obs_ys, obs_xs = np.where(o_arr[:, :, 3] > 0)
obs_x0, obs_x1 = int(obs_xs.min()), int(obs_xs.max() + 1)
obs_y0, obs_y1 = int(obs_ys.min()), int(obs_ys.max() + 1)
obs_clean = Image.fromarray(o_arr, 'RGBA').crop((obs_x0, obs_y0, obs_x1, obs_y1))
obs_clean.save(f'{PARTS_DIR}/costume/costume_astral_observer.png')
obs_w, obs_h = obs_clean.size

# Navel anchor is (256, 350)
obs_origin_x = 256 - obs_x0
obs_origin_y = 350 - obs_y0
print(f"Saved costume_astral_observer.png: {obs_w}x{obs_h}, origin=[{obs_origin_x}, {obs_origin_y}]")

# -------------------------------------------------------------
# 6. 武器 (wpn_astral_staff) - 精修去背、消除邊緣雜色與半透明噪點
# -------------------------------------------------------------
wpn_512 = Image.open(f'{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff_512.png').convert('RGBA')
w_arr = np.array(wpn_512)

# 移除左上方孤立肩甲碎片 (x < 360, y < 240)
w_arr[:240, :360] = [0, 0, 0, 0]

# 移除下方懸空拖尾雜點 (y > 435)
w_arr[435:, :] = [0, 0, 0, 0]

# 橋接木質法杖手柄處自然紋理與形體 (y in 382..398, x in 351..358)
for y in range(382, 398):
    for x in range(351, 358):
        if w_arr[y, x, 3] > 0:
            w_arr[y, x, 3] = 255
            if w_arr[y, x, 0] < 50:
                w_arr[y, x] = [105, 65, 45, 255]

# 去除邊緣雜色與低 alpha 雜點 (alpha < 60)
w_arr[w_arr[:, :, 3] < 60] = [0, 0, 0, 0]

# 清理握柄交界處深褐色遮罩雜點與半透明噪點
dirty = (w_arr[:, :, 3] > 0) & (w_arr[:, :, 3] < 150) & (w_arr[:, :, 0] < 90) & (w_arr[:, :, 1] < 70) & (w_arr[:, :, 2] < 60)
w_arr[dirty] = [0, 0, 0, 0]

# 邊緣像素實體化 (cel-shaded clean edge)
w_arr[w_arr[:, :, 3] >= 110, 3] = 255

# 僅保留法杖與手部主體連通區塊
w_mask = w_arr[:, :, 3] > 0
w_labeled, w_num = label(w_mask)
if w_num > 1:
    w_sizes = [np.sum(w_labeled == i) for i in range(1, w_num + 1)]
    w_main = np.argmax(w_sizes) + 1
    w_arr[w_labeled != w_main] = [0, 0, 0, 0]

# 取得非透明像素範圍並裁切緊湊 Sprite
wpn_ys, wpn_xs = np.where(w_arr[:, :, 3] > 0)
wpn_x0, wpn_x1 = int(wpn_xs.min()), int(wpn_xs.max() + 1)
wpn_y0, wpn_y1 = int(wpn_ys.min()), int(wpn_ys.max() + 1)
clean_staff = Image.fromarray(w_arr, 'RGBA').crop((wpn_x0, wpn_y0, wpn_x1, wpn_y1))
clean_staff.save(f'{PARTS_DIR}/weapon/wpn_astral_staff.png')
wpn_w, wpn_h = clean_staff.size

# Hand anchor is (358, 363)
wpn_origin_x = 358 - wpn_x0
wpn_origin_y = 363 - wpn_y0
print(f"Saved wpn_astral_staff.png: {wpn_w}x{wpn_h}, origin=[{wpn_origin_x}, {wpn_origin_y}]")

# -------------------------------------------------------------
# 7. 更新 maple_paperdoll_fox.json 部件尺寸與 origin
# -------------------------------------------------------------
with open(SPEC_JSON_PATH, 'r', encoding='utf-8') as f:
    spec = json.load(f)

# Update costume_astral_observer
spec['parts']['costume']['items']['costume_astral_observer']['width'] = obs_w
spec['parts']['costume']['items']['costume_astral_observer']['height'] = obs_h
spec['parts']['costume']['items']['costume_astral_observer']['origin'] = [obs_origin_x, obs_origin_y]

# Update wpn_astral_staff
spec['parts']['weapon']['items']['wpn_astral_staff']['width'] = wpn_w
spec['parts']['weapon']['items']['wpn_astral_staff']['height'] = wpn_h
spec['parts']['weapon']['items']['wpn_astral_staff']['origin'] = [wpn_origin_x, wpn_origin_y]

with open(SPEC_JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(spec, f, indent=2, ensure_ascii=False)

print("Updated maple_paperdoll_fox.json with refined part dimensions and origins.")
