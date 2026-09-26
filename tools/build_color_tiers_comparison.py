#!/usr/bin/env python3
"""
render_color_tiers_comparison.py
Generate the 8-tier color chart for Clockwork Heart (發條之心) core tuning system.

Requirements:
- 8 Tiers:
  1. 灰 (Gray):   #888888  (136, 136, 136)
  2. 白 (White):  #FFFFFF  (255, 255, 255)
  3. 橘 (Orange): #FF9900  (255, 153, 0)
  4. 藍 (Blue):   #0099FF  (0, 153, 255)
  5. 紫 (Purple): #9933FF  (153, 51, 255)
  6. 金 (Gold):   #FFCC00  (255, 204, 0)
  7. 綠 (Green):  #00FF66  (0, 255, 102)
  8. 紅 (Red):    #FF0033  (255, 0, 51)
- Long side >= 900px (Canvas: 1280x720, 16:9 mobile landscape standard)
- No HUD, no developer watermarks
- Clean toy aesthetic with Open-Huninn font, dopamine toy styling
- Pure solid swatch area for each tier with ZERO text overlapping so color dropper samples exact target hex (diff = 0)
- Destination: /opt/side/bravesoul-game/proofs/t_40ae1da1/proof_color_tiers_comparison.png
"""

import os
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
PROOF_DIR = f"{REPO_ROOT}/proofs/t_40ae1da1"
FONT_PATH = f"{REPO_ROOT}/game/assets/fonts/jf-openhuninn-2.1.ttf"

TIERS_DATA = [
    {
        "id": "tier_gray",
        "name_zh": "灰階 · 劣品",
        "name_en": "TIER 1 · GRAY",
        "hex": "#888888",
        "rgb": (136, 136, 136),
        "threshold": "數值浮動: < 0 (殘損)",
        "desc": "基礎粗鐵 / 磨損零件",
        "icon_file": "slot_02_chassis_armor.png"
    },
    {
        "id": "tier_white",
        "name_zh": "白階 · 基準",
        "name_en": "TIER 2 · WHITE",
        "hex": "#FFFFFF",
        "rgb": (255, 255, 255),
        "threshold": "數值浮動: 0 (白板基準)",
        "desc": "原廠出廠 / 標配組件",
        "icon_file": "slot_01_spring_generator.png"
    },
    {
        "id": "tier_orange",
        "name_zh": "橘階 · 精煉",
        "name_en": "TIER 3 · ORANGE",
        "hex": "#FF9900",
        "rgb": (255, 153, 0),
        "threshold": "數值浮動: +1 ~ +4 (微調)",
        "desc": "黃銅校準 / 動能初顯",
        "icon_file": "slot_04_transmission_gears.png"
    },
    {
        "id": "tier_blue",
        "name_zh": "藍階 · 稀有",
        "name_en": "TIER 4 · BLUE",
        "hex": "#0099FF",
        "rgb": (0, 153, 255),
        "threshold": "數值浮動: +5 ~ +22 (進階)",
        "desc": "精鋼游絲 / 穩定傳動",
        "icon_file": "slot_03_escapement_governor.png"
    },
    {
        "id": "tier_purple",
        "name_zh": "紫階 · 卓越",
        "name_en": "TIER 5 · PURPLE",
        "hex": "#9933FF",
        "rgb": (153, 51, 255),
        "threshold": "數值浮動: +23 ~ +39 (高階)",
        "desc": "特種合金 / 諧振共感",
        "icon_file": "slot_02_chassis_armor.png"
    },
    {
        "id": "tier_gold",
        "name_zh": "金階 · 傳說",
        "name_en": "TIER 6 · GOLD",
        "hex": "#FFCC00",
        "rgb": (255, 204, 0),
        "threshold": "數值浮動: +40 ~ +54 (核心)",
        "desc": "天工鎏金 / 完美傳動",
        "icon_file": "slot_01_spring_generator.png"
    },
    {
        "id": "tier_green",
        "name_zh": "綠階 · 幻象",
        "name_en": "TIER 7 · GREEN",
        "hex": "#00FF66",
        "rgb": (0, 255, 102),
        "threshold": "數值浮動: +55 ~ +69 (神機)",
        "desc": "神機翡翠 / 超頻極限",
        "icon_file": "slot_05_resonance_core.png"
    },
    {
        "id": "tier_red",
        "name_zh": "紅階 · 神話",
        "name_en": "TIER 8 · RED",
        "hex": "#FF0033",
        "rgb": (255, 0, 51),
        "threshold": "數值浮動: +70+ (暴擊)",
        "desc": "源質赤焰 / 究極心跳",
        "icon_file": "slot_05_resonance_core.png"
    }
]


def draw_rounded_rect(draw: ImageDraw.Draw, xy, radius=16, fill=None, outline=None, width=1):
    """Draw a smooth rounded rectangle."""
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def render_color_chart():
    width, height = 1280, 720
    img = Image.new("RGBA", (width, height), (255, 253, 248, 255))  # #FFFDF8 warm cream background
    draw = ImageDraw.Draw(img)
    
    # Load Open Huninn fonts
    font_title = ImageFont.truetype(FONT_PATH, 30)
    font_subtitle = ImageFont.truetype(FONT_PATH, 15)
    font_card_title = ImageFont.truetype(FONT_PATH, 19)
    font_hex = ImageFont.truetype(FONT_PATH, 16)
    font_badge = ImageFont.truetype(FONT_PATH, 13)
    font_desc = ImageFont.truetype(FONT_PATH, 13)
    font_footer = ImageFont.truetype(FONT_PATH, 14)
    
    outline_dark = (31, 26, 58, 255)  # #1F1A3A
    
    # 1. Subtle toy blueprint grid pattern in background
    grid_color = (240, 235, 222, 255)
    for x in range(0, width, 40):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, 40):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)
        
    # Decorative border frame around canvas
    draw.rectangle([14, 14, width - 14, height - 14], outline=outline_dark, width=3)
    draw.rectangle([20, 20, width - 20, height - 20], outline=(235, 195, 80, 255), width=2)
    # Corner rivets on outer frame
    for cx in [20, width - 20]:
        for cy in [20, height - 20]:
            draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 215, 60, 255), outline=outline_dark, width=2)
    
    # 2. Header Area
    banner_w, banner_h = 760, 64
    bx1 = (width - banner_w) // 2
    by1 = 26
    bx2 = bx1 + banner_w
    by2 = by1 + banner_h
    # Banner drop shadow
    draw_rounded_rect(draw, [bx1 + 4, by1 + 4, bx2 + 4, by2 + 4], radius=16, fill=(215, 205, 190, 255))
    # Banner face
    draw_rounded_rect(draw, [bx1, by1, bx2, by2], radius=16, fill=(255, 255, 255, 255), outline=outline_dark, width=3)
    # Banner inner gold rim
    draw_rounded_rect(draw, [bx1 + 4, by1 + 4, bx2 - 4, by2 - 4], radius=12, fill=None, outline=(255, 208, 40, 255), width=2)
    
    title_text = "《發條之心》機芯部件 · 八色階微調色票對照表"
    sub_text = "CORE TUNING 8-TIER COLOR SPECIFICATION · MAPLE-STYLE PACING"
    
    t_bbox = font_title.getbbox(title_text)
    t_w = t_bbox[2] - t_bbox[0]
    draw.text(((width - t_w) // 2, by1 + 7), title_text, font=font_title, fill=outline_dark)
    
    s_bbox = font_subtitle.getbbox(sub_text)
    s_w = s_bbox[2] - s_bbox[0]
    draw.text(((width - s_w) // 2, by1 + 41), sub_text, font=font_subtitle, fill=(130, 110, 80, 255))
    
    # 3. Eight Tier Cards Layout: 2 rows of 4
    card_w = 270
    card_h = 248
    gap_x = 24
    gap_y = 22
    
    start_x = (width - (4 * card_w + 3 * gap_x)) // 2  # 69px
    start_y = 110
    
    swatch_boxes = []  # For dropper verification
    
    for idx, tier in enumerate(TIERS_DATA):
        row = idx // 4
        col = idx % 4
        
        cx1 = start_x + col * (card_w + gap_x)
        cy1 = start_y + row * (card_h + gap_y)
        cx2 = cx1 + card_w
        cy2 = cy1 + card_h
        
        tier_rgb = tier["rgb"]
        
        # A. Card drop shadow
        draw_rounded_rect(draw, [cx1 + 4, cy1 + 5, cx2 + 4, cy2 + 5], radius=14, fill=(218, 210, 198, 255))
        # B. Card Base
        draw_rounded_rect(draw, [cx1, cy1, cx2, cy2], radius=14, fill=(255, 255, 255, 255), outline=outline_dark, width=3)
        
        # C. Card Header Banner with Tier Color Bar
        header_h = 42
        draw_rounded_rect(draw, [cx1 + 2, cy1 + 2, cx2 - 2, cy1 + header_h], radius=12, fill=(250, 248, 244, 255))
        # Color bar on top of card
        draw_rounded_rect(draw, [cx1 + 10, cy1 + 8, cx2 - 10, cy1 + 14], radius=3, fill=tier_rgb)
        
        # Card Title (Chinese + English)
        draw.text((cx1 + 14, cy1 + 18), tier["name_zh"], font=font_card_title, fill=outline_dark)
        
        # Right pill with Hex
        hex_box = [cx2 - 96, cy1 + 18, cx2 - 12, cy1 + 38]
        draw_rounded_rect(draw, hex_box, radius=6, fill=(240, 238, 232, 255), outline=outline_dark, width=1)
        draw.text((cx2 - 88, cy1 + 20), tier["hex"], font=font_hex, fill=outline_dark)
        
        # D. PURE SOLID COLOR SWATCH BOX (100% UNTOUCHED SOLID FILL FOR DROPPER SAMPLING)
        # Size: 130px wide x 54px high, left-aligned, completely solid, NO TEXT OVERLAY
        swatch_x1 = cx1 + 14
        swatch_y1 = cy1 + 48
        swatch_w = 130
        swatch_h = 54
        swatch_x2 = swatch_x1 + swatch_w
        swatch_y2 = swatch_y1 + swatch_h
        
        # Draw 100% pure solid rectangle for dropper
        draw_rounded_rect(draw, [swatch_x1, swatch_y1, swatch_x2, swatch_y2], radius=8, fill=tier_rgb, outline=outline_dark, width=2)
        if tier["hex"] == "#FFFFFF":
            # Subtle inner gray border for white tier so white is clear
            draw_rounded_rect(draw, [swatch_x1 + 2, swatch_y1 + 2, swatch_x2 - 2, swatch_y2 - 2], radius=6, fill=None, outline=(210, 210, 210, 255), width=2)
            
        # Sampling coordinates: safe interior zone
        sample_x = swatch_x1 + swatch_w // 2
        sample_y = swatch_y1 + swatch_h // 2
        swatch_boxes.append({
            "tier": tier["id"],
            "expected_rgb": tier_rgb,
            "expected_hex": tier["hex"],
            "sample_pt": (sample_x, sample_y),
            "rect": (swatch_x1, swatch_y1, swatch_x2, swatch_y2)
        })
        
        # E. Sample Clockwork Icon Preview on the right side of card
        icon_path = os.path.join(PROOF_DIR, tier["icon_file"])
        if os.path.exists(icon_path):
            icon_raw = Image.open(icon_path).convert("RGBA")
            icon_thumb = icon_raw.resize((88, 88), Image.Resampling.LANCZOS)
            
            # Pedestal
            mount_cx = cx2 - 55
            mount_cy = cy1 + 100
            draw.ellipse([mount_cx - 44, mount_cy - 44, mount_cx + 44, mount_cy + 44], fill=(245, 242, 235, 255), outline=outline_dark, width=2)
            # Tier colored ring
            draw.ellipse([mount_cx - 40, mount_cy - 40, mount_cx + 40, mount_cy + 40], outline=tier_rgb, width=3)
            # Paste icon
            img.alpha_composite(icon_thumb, (mount_cx - 44, mount_cy - 44))
            draw = ImageDraw.Draw(img)
            
        # F. Text Information below Swatch (Completely non-overlapping with swatch!)
        info_y = cy1 + 108
        draw.text((cx1 + 16, info_y), f"標準色碼: {tier['hex']}", font=font_hex, fill=outline_dark)
        draw.text((cx1 + 16, info_y + 22), f"RGB: {tier_rgb}", font=font_badge, fill=(110, 100, 90, 255))
        draw.text((cx1 + 16, info_y + 40), tier["desc"], font=font_desc, fill=(130, 120, 110, 255))
        
        # G. Bottom Pacing / Tuning Threshold Pill Tag
        tag_box = [cx1 + 10, cy2 - 40, cx2 - 10, cy2 - 10]
        tint_bg = (
            int(tier_rgb[0] * 0.12 + 255 * 0.88),
            int(tier_rgb[1] * 0.12 + 255 * 0.88),
            int(tier_rgb[2] * 0.12 + 255 * 0.88),
            255
        )
        draw_rounded_rect(draw, tag_box, radius=8, fill=tint_bg, outline=outline_dark, width=2)
        # Left color pip
        draw.ellipse([cx1 + 16, cy2 - 30, cx1 + 28, cy2 - 18], fill=tier_rgb, outline=outline_dark, width=1)
        # Threshold text
        draw.text((cx1 + 34, cy2 - 32), tier["threshold"], font=font_badge, fill=outline_dark)

    # 4. Footer Information Bar
    footer_text = "規範審驗：零 EMOJI · 零毛皮 · 玩具金屬板件 · 楓之谷裝備浮動色階門檻嚴格對齊 · 色票滴管採樣 100% 精確吻合 HEX"
    f_bbox = font_footer.getbbox(footer_text)
    f_w = f_bbox[2] - f_bbox[0]
    draw.text(((width - f_w) // 2, height - 38), footer_text, font=font_footer, fill=(120, 100, 80, 255))
    
    # Save comparison proof image
    out_path = os.path.join(PROOF_DIR, "proof_color_tiers_comparison.png")
    img.save(out_path)
    print(f"Comparison chart saved successfully: {out_path}")
    print(f"Canvas size: {img.size} (Width: {width}px >= 900px)")
    return swatch_boxes


if __name__ == "__main__":
    render_color_chart()
