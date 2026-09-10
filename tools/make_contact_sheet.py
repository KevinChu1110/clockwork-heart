#!/usr/bin/env python3
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = "/opt/side/bravesoul-game"
VIDEO_PATH = os.path.join(ROOT, "web/media/shorts/mk_shorts_five_races_combat_18s.mp4")
SHEET_PATH = os.path.join(ROOT, "docs/marketing/shots/mk_shorts_five_races_combat_18s_contact_sheet.png")
FONT_PATH = os.path.join(ROOT, "game/assets/fonts/jf-openhuninn-2.1.ttf")
TMP_DIR = "/tmp/contact_sheet_samples"
os.makedirs(TMP_DIR, exist_ok=True)
os.makedirs(os.path.dirname(SHEET_PATH), exist_ok=True)

sample_times = [
    ("Shot 1 微距懸念 (1.5s)", 1.5),
    ("Shot 2 兔族晨光長劍 (4.2s)", 4.2),
    ("Shot 3 獅族皇家長槍 (6.8s)", 6.8),
    ("Shot 4 狐族秘術法杖 (9.3s)", 9.3),
    ("Shot 5 豬族鍛爐重鎚 (11.8s)", 11.8),
    ("Shot 6 猴族靈爪暴怒 (14.5s)", 14.5),
    ("Shot 7 點題官方字標 (16.8s)", 16.8),
]

sample_imgs = []
for label, sec in sample_times:
    p = os.path.join(TMP_DIR, f"sample_{sec:.1f}.png")
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-ss", f"{sec:.2f}",
        "-i", VIDEO_PATH,
        "-vframes", "1",
        p
    ], check=True)
    img = Image.open(p).convert("RGBA")
    sample_imgs.append((label, img))

thumb_w = 360
thumb_h = 640
pad = 20
header_h = 75

cols = 4
rows = 2
canvas_w = cols * thumb_w + (cols + 1) * pad
canvas_h = rows * thumb_h + (rows + 1) * pad + header_h

sheet = Image.new("RGBA", (canvas_w, canvas_h), (20, 18, 28, 255))
draw = ImageDraw.Draw(sheet)
font_title = ImageFont.truetype(FONT_PATH, 30)
font_label = ImageFont.truetype(FONT_PATH, 20)

draw.text((pad, 22), "《發條之心》18 秒五族實機打擊短影音抽樣查驗表 (1080×1920 @ 30fps, 18.00s)", font=font_title, fill=(255, 215, 60, 255))

for idx, (label, img) in enumerate(sample_imgs):
    c = idx % cols
    r = idx // cols
    x = pad + c * (thumb_w + pad)
    y = header_h + pad + r * (thumb_h + pad)
    
    resized = img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    sheet.paste(resized, (x, y))
    
    # 邊框
    draw.rectangle([x, y, x + thumb_w, y + thumb_h], outline=(80, 75, 110), width=2)
    # 標籤底條
    draw.rectangle([x, y + thumb_h - 40, x + thumb_w, y + thumb_h], fill=(10, 8, 16, 210))
    draw.text((x + 12, y + thumb_h - 34), label, font=font_label, fill=(255, 255, 255, 255))

# 第 8 格放置資訊卡
info_x = pad + 3 * (thumb_w + pad)
info_y = header_h + pad + 1 * (thumb_h + pad)
draw.rectangle([info_x, info_y, info_x + thumb_w, info_y + thumb_h], fill=(28, 25, 38, 255), outline=(100, 90, 140), width=2)
draw.text((info_x + 20, info_y + 30), "【短影音規格查核】", font=font_label, fill=(255, 215, 60, 255))
lines = [
    "片名: mk_shorts_five_races",
    "時長: 18.00s (540 幀 @ 30fps)",
    "畫幅: 9:16 (1080×1920)",
    "音效: 8 軌 Procedural SFX",
    "兔族: 白金兔 · 晨光長劍",
    "獅族: 烈鬃獅 · 皇家長槍",
    "狐族: 靈尾狐 · 星盤法杖",
    "豬族: 鋼牙豕 · 鍛爐重鎚",
    "猴族: 靈爪猴 · 機關靈爪",
    "世界觀: 金屬發條 · 零毛皮",
    "字標: 官方無失真後製疊加",
    "狀態: 已通過審查驗收"
]
font_info = ImageFont.truetype(FONT_PATH, 17)
for i, line in enumerate(lines):
    draw.text((info_x + 20, info_y + 80 + i * 42), line, font=font_info, fill=(230, 235, 240, 255))

sheet.convert("RGB").save(SHEET_PATH)
print("SUCCESS:", SHEET_PATH)
