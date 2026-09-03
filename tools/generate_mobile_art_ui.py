import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT_DIR = "game/assets/sprites/ui/mobile"
os.makedirs(OUT_DIR, exist_ok=True)

FONT_PATH = "game/assets/fonts/NotoSansTC-Regular.otf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

def draw_large_sword_icon(draw_layer, cx, cy, size):
    """繪製大型、帶銀白開刃、金色護手與厚描邊的交叉雙劍 (與字體同高)"""
    s = size
    stroke = (45, 15, 10, 255)
    
    for angle in [-40, 40]:
        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        # 劍刃
        p1 = (cx - cos_a * s * 0.75, cy - sin_a * s * 0.75)
        p2 = (cx + cos_a * s * 0.55, cy + sin_a * s * 0.55)
        
        # 深色粗描邊
        draw_layer.line([p1, p2], fill=stroke, width=int(s * 0.32))
        # 銀白鋼刃
        draw_layer.line([p1, p2], fill=(230, 245, 255, 255), width=int(s * 0.20))
        # 刃中央亮白高光
        draw_layer.line([p1, p2], fill=(255, 255, 255, 255), width=int(s * 0.08))
        
        # 金色劍格護手
        h1 = (cx + cos_a * s * 0.22 - sin_a * s * 0.32, cy + sin_a * s * 0.22 + cos_a * s * 0.32)
        h2 = (cx + cos_a * s * 0.22 + sin_a * s * 0.32, cy + sin_a * s * 0.22 - cos_a * s * 0.32)
        draw_layer.line([h1, h2], fill=stroke, width=int(s * 0.26))
        draw_layer.line([h1, h2], fill=(255, 215, 45, 255), width=int(s * 0.16))
        
        # 劍柄末端金色球飾
        pommel = (cx + cos_a * s * 0.65, cy + sin_a * s * 0.65)
        pr = s * 0.14
        draw_layer.ellipse([pommel[0]-pr, pommel[1]-pr, pommel[0]+pr, pommel[1]+pr], fill=stroke)
        draw_layer.ellipse([pommel[0]-pr*0.6, pommel[1]-pr*0.6, pommel[0]+pr*0.6, pommel[1]+pr*0.6], fill=(255, 180, 25, 255))

def create_true_commercial_button(
    text,
    width=260,
    height=64,
    top_color=(255, 225, 65),       # 頂部明黃
    bot_color=(255, 115, 10),       # 底部熱血暖橘
    bevel_color=(185, 60, 0),       # 3D 實體厚槽深色
    stroke_color=(40, 15, 20),      # 深暖褐紫邊
    has_icon="swords",
    font_size=24
):
    scale = 2
    w = width * scale
    h = height * scale
    radius = int(22 * scale)
    bevel_h = int(8 * scale) # 實體加厚 8px

    # 主透明畫布
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    # 1. 外部環境立體投影 (Drop Shadow)
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_box = (6 * scale, 10 * scale, w - 6 * scale, h)
    s_draw.rounded_rectangle(s_box, radius=radius, fill=(15, 8, 30, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(4 * scale))
    canvas = Image.alpha_composite(canvas, shadow)

    # 2. 3D 實體厚底座 (Extrusion Bevel Base)
    base_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(base_layer)
    base_box = (4 * scale, 4 * scale, w - 4 * scale, h - 4 * scale)
    b_draw.rounded_rectangle(base_box, radius=radius, fill=bevel_color + (255,))
    b_draw.rounded_rectangle(base_box, radius=radius, outline=stroke_color + (255,), width=int(3.5 * scale))
    canvas = Image.alpha_composite(canvas, base_layer)

    # 3. 正面飽滿漸層 (Top Gradient Face)
    face_h = h - bevel_h - 4 * scale
    face_box = (4 * scale, 4 * scale, w - 4 * scale, face_h)
    face_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    f_draw = ImageDraw.Draw(face_layer)

    for y in range(4 * scale, face_h + 1):
        f = (y - 4 * scale) / float(face_h - 4 * scale + 1)
        f = max(0.0, min(1.0, f))
        r = int(top_color[0] * (1 - f) + bot_color[0] * f)
        g = int(top_color[1] * (1 - f) + bot_color[1] * f)
        b = int(top_color[2] * (1 - f) + bot_color[2] * f)
        f_draw.line([(4 * scale, y), (w - 4 * scale, y)], fill=(r, g, b, 255))

    # 限制在正面圓角區域
    face_mask = Image.new("L", (w, h), 0)
    fm_draw = ImageDraw.Draw(face_mask)
    fm_draw.rounded_rectangle(face_box, radius=radius, fill=255)
    
    # 遮罩正面圖層
    final_face = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    final_face.paste(face_layer, (0, 0), face_mask)
    canvas = Image.alpha_composite(canvas, final_face)

    # 4. 頂部柔和羽化果凍月牙高光 (Curved Soft Jelly Highlight)
    glow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gl_draw = ImageDraw.Draw(glow_layer)
    glow_box = (8 * scale, 6 * scale, w - 8 * scale, int(face_h * 0.65))
    gl_draw.ellipse(glow_box, fill=(255, 255, 255, 110))
    glow_blurred = glow_layer.filter(ImageFilter.GaussianBlur(3 * scale))
    
    # 限制在正面內
    final_glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    final_glow.paste(glow_blurred, (0, 0), face_mask)
    canvas = Image.alpha_composite(canvas, final_glow)

    # 5. 正面頂部高光輪廓線 (Rim Light)
    rim_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rim_layer)
    r_draw.rounded_rectangle(face_box, radius=radius, outline=(255, 255, 220, 160), width=int(1.5 * scale))
    canvas = Image.alpha_composite(canvas, rim_layer)

    # 6. 外層主輪廓
    outline_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    o_draw = ImageDraw.Draw(outline_layer)
    o_draw.rounded_rectangle(base_box, radius=radius, outline=stroke_color + (255,), width=int(3.5 * scale))
    canvas = Image.alpha_composite(canvas, outline_layer)

    # 7. 計算文字與大圖標佈局 (佔滿 75% 寬度)
    font = ImageFont.truetype(FONT_PATH, int(font_size * scale))
    dummy_draw = ImageDraw.Draw(canvas)
    bbox = dummy_draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    icon_sz = int(th * 1.3) if has_icon else 0 # 圖標與文字等高！
    gap = int(10 * scale) if has_icon else 0
    total_w = tw + icon_sz + gap
    start_x = (w - total_w) // 2
    content_cy = int(face_h * 0.5)

    # 8. 繪製大圖標
    if has_icon == "swords":
        icon_cx = start_x + icon_sz // 2
        icon_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        i_draw = ImageDraw.Draw(icon_layer)
        draw_large_sword_icon(i_draw, icon_cx, content_cy, size=int(icon_sz * 0.7))
        canvas = Image.alpha_composite(canvas, icon_layer)

    tx = start_x + icon_sz + gap
    ty = content_cy - th // 2 - int(3 * scale)

    # 9. 渲染文字層 (投影 -> 4.5px 粗描邊 -> 金黃漸層面 -> 頂部亮白內邊)
    txt_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(txt_layer)

    # (a) 文字投影
    for dy in range(int(1.5 * scale), int(4.5 * scale)):
        t_draw.text((tx, ty + dy), text, font=font, fill=(35, 15, 20, 220))

    # (b) 文字厚描邊 (4.5px)
    sw = int(4.5 * scale)
    for ox in range(-sw, sw + 1):
        for oy in range(-sw, sw + 1):
            if ox*ox + oy*oy <= sw*sw:
                t_draw.text((tx + ox, ty + oy), text, font=font, fill=stroke_color + (255,))

    # (c) 文字漸層面 (頂金黃 -> 底暖橘紅)
    glyph_mask = Image.new("L", (w, h), 0)
    gm_draw = ImageDraw.Draw(glyph_mask)
    gm_draw.text((tx, ty), text, font=font, fill=255)

    txt_grad = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    tg_draw = ImageDraw.Draw(txt_grad)
    for y in range(int(ty), int(ty + th + 6 * scale)):
        f = (y - ty) / float(th + 1)
        f = max(0.0, min(1.0, f))
        r = int(255 * (1 - f) + 255 * f)
        g = int(248 * (1 - f) + 140 * f)
        b = int(120 * (1 - f) + 15 * f)
        tg_draw.line([(tx - 6*scale, y), (tx + tw + 6*scale, y)], fill=(r, g, b, 255))

    final_txt = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    final_txt.paste(txt_grad, (0, 0), glyph_mask)

    # (d) 頂部 1.5px 亮白內邊高光
    t_rim = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    tr_draw = ImageDraw.Draw(t_rim)
    tr_draw.text((tx, ty - int(1.5 * scale)), text, font=font, fill=(255, 255, 255, 230))
    final_txt.paste(t_rim, (0, 0), glyph_mask)

    # 組合文字到畫布
    canvas = Image.alpha_composite(canvas, txt_layer)
    canvas = Image.alpha_composite(canvas, final_txt)

    # Lanczos 高精度縮小回原尺寸
    return canvas.resize((width, height), Image.Resampling.LANCZOS)

# 生成商業手遊出征按鈕
btn_adv = create_true_commercial_button(
    "出征冒險！", width=280, height=68,
    top_color=(255, 225, 65), bot_color=(255, 115, 10),
    bevel_color=(185, 60, 0), stroke_color=(40, 15, 20),
    has_icon="swords", font_size=23
)
btn_adv.save(f"{OUT_DIR}/btn_go_adventure.png")

# 生成薄荷綠簽到按鈕
btn_sign = create_true_commercial_button(
    "今日簽到與委託", width=280, height=62,
    top_color=(100, 240, 140), bot_color=(25, 175, 75),
    bevel_color=(15, 115, 45), stroke_color=(15, 40, 25),
    has_icon="", font_size=19
)
btn_sign.save(f"{OUT_DIR}/btn_sign_daily.png")

# 生成十連聚魂按鈕
btn_draw10 = create_true_commercial_button(
    "聚魂十次", width=220, height=56,
    top_color=(255, 225, 75), bot_color=(255, 130, 15),
    bevel_color=(175, 65, 0), stroke_color=(45, 15, 25),
    has_icon="", font_size=20
)
btn_draw10.save(f"{OUT_DIR}/btn_draw_10.png")

# 生成 BOSS 開戰按鈕
btn_boss = create_true_commercial_button(
    "開戰 (⚡3)", width=145, height=52,
    top_color=(255, 185, 50), bot_color=(255, 75, 20),
    bevel_color=(175, 35, 10), stroke_color=(45, 15, 20),
    has_icon="", font_size=18
)
btn_boss.save(f"{OUT_DIR}/btn_boss_battle.png")

# 生成一般關卡開戰按鈕
btn_norm = create_true_commercial_button(
    "開戰 (⚡1)", width=145, height=50,
    top_color=(100, 205, 255), bot_color=(30, 130, 240),
    bevel_color=(15, 75, 165), stroke_color=(15, 35, 65),
    has_icon="", font_size=18
)
btn_norm.save(f"{OUT_DIR}/btn_normal_battle.png")

print("All true commercial graphic buttons generated successfully!")
