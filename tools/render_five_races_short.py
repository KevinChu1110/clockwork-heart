#!/usr/bin/env python3
import os
import math
import subprocess
from PIL import Image, ImageFilter, ImageDraw, ImageFont

ROOT = "/opt/side/bravesoul-game"
OUT_DIR = os.path.join(ROOT, "proofs/render_18s/frames")
os.makedirs(OUT_DIR, exist_ok=True)

WIDTH = 1080
HEIGHT = 1920
FPS = 30

FONT_PATH = os.path.join(ROOT, "game/assets/fonts/jf-openhuninn-2.1.ttf")
TITLE_PLATE_PATH = os.path.join(ROOT, "branding/title_plate.png")
LOGO_PATH = os.path.join(ROOT, "branding/logo_cn.png")
KEY_VISUAL_PATH = os.path.join(ROOT, "branding/key_visual_main.png")
FRAMES_BASE = os.path.join(ROOT, "proofs/five_races_frames")

def render_shot1():
    print(">>> Rendering Shot 1 (0.0s - 3.0s, 90 frames)...")
    im = Image.open(KEY_VISUAL_PATH).convert("RGBA")
    # crop=222:396:455:372
    crop_x = 455
    crop_y = 372
    crop_w = 222
    crop_h = 396
    
    base_crop = im.crop((crop_x, crop_y, crop_x + crop_w, crop_y + crop_h))
    
    for i in range(90):
        t = i / 89.0
        # Dolly In 105%: scale from 1.00 to 1.05
        scale = 1.00 + 0.05 * t
        cw = crop_w / scale
        ch = crop_h / scale
        cx = crop_x + (crop_w - cw) * 0.5
        cy = crop_y + (crop_h - ch) * 0.5
        frame_crop = im.crop((int(cx), int(cy), int(cx + cw), int(cy + ch)))
        frame_scaled = frame_crop.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
        
        # 光芒暴亮轉場：最後 6 幀淡入白色
        if i >= 84:
            flash_alpha = (i - 84) / 5.0 * 0.75
            white = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, int(255 * flash_alpha)))
            frame_scaled = Image.alpha_composite(frame_scaled, white)
            
        out_f = os.path.join(OUT_DIR, f"frame_{i:04d}.png")
        if os.path.exists(out_f) and os.path.getsize(out_f) > 1000:
            continue
        frame_scaled.convert("RGB").save(out_f)

def render_combat_shot(race, start_frame, max_zoom, pan_y=0.0):
    rdir = os.path.join(FRAMES_BASE, race)
    print(f">>> Rendering Combat Shot: {race} (frames {start_frame} - {start_frame + 74})...")
    
    for i in range(75):
        raw_path = os.path.join(rdir, f"frame_{i:04d}.png")
        raw_img = Image.open(raw_path).convert("RGBA")
        
        # 1. 底層高斯模糊背景 (放大填滿 1080x1920)
        # 保持長寬比放大並居中裁切
        bg_scale = max(WIDTH / 1280.0, HEIGHT / 720.0)
        bg_w = int(1280 * bg_scale)
        bg_h = int(720 * bg_scale)
        bg = raw_img.resize((bg_w, bg_h), Image.Resampling.BILINEAR)
        bg_x = (bg_w - WIDTH) // 2
        bg_y = (bg_h - HEIGHT) // 2
        bg = bg.crop((bg_x, bg_y, bg_x + WIDTH, bg_y + HEIGHT))
        bg = bg.filter(ImageFilter.GaussianBlur(radius=30))
        
        # 壓暗底層，增加對比
        darkener = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 80))
        bg = Image.alpha_composite(bg, darkener)
        
        # 2. 中央戰鬥主畫面配合推鏡
        t = i / 74.0
        scale = 1.00 + (max_zoom - 1.00) * t
        
        # 主畫面標準寬度為 WIDTH (1080)，標準高度為 1080 * 720 / 1280 = 607.5
        main_w = int(WIDTH * scale)
        main_h = int(607.5 * scale)
        
        scaled_raw = raw_img.resize((main_w, main_h), Image.Resampling.LANCZOS)
        
        # 居中放置，pan_y 調整中心偏移
        center_y = int(HEIGHT * 0.5 + pan_y * 100 * t)
        main_x = (WIDTH - main_w) // 2
        main_y = center_y - main_h // 2
        
        # 繪製主畫面輕微投影與裝飾框
        shadow = Image.new("RGBA", (main_w + 30, main_h + 30), (0, 0, 0, 160))
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=15))
        bg.paste(shadow, (main_x - 15, main_y - 15), shadow)
        
        bg.paste(scaled_raw, (main_x, main_y), scaled_raw)
        
        # 在第一幀有輕微光芒轉場
        if i < 4 and race == "rabbit":
            white_alpha = (4 - i) / 4.0 * 0.5
            white = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, int(255 * white_alpha)))
            bg = Image.alpha_composite(bg, white)
            
        frame_idx = start_frame + i
        out_f = os.path.join(OUT_DIR, f"frame_{frame_idx:04d}.png")
        if os.path.exists(out_f) and os.path.getsize(out_f) > 1000:
            continue
        bg.convert("RGB").save(out_f)

def render_shot7(start_frame):
    print(f">>> Rendering Shot 7: CTA End Plate (frames {start_frame} - {start_frame + 74})...")
    plate_raw = Image.open(TITLE_PLATE_PATH).convert("RGBA")
    plate_base = plate_raw.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    
    logo_raw = Image.open(LOGO_PATH).convert("RGBA")
    logo_w = int(WIDTH * 0.78)
    logo_h = int(logo_w * 640 / 1024)
    logo_scaled = logo_raw.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
    
    font_slogan = ImageFont.truetype(FONT_PATH, 42)
    font_sub = ImageFont.truetype(FONT_PATH, 28)
    
    for i in range(75):
        t = i / 74.0
        scale = 1.00 + 0.02 * t
        
        # 緩推
        w_curr = int(WIDTH * scale)
        h_curr = int(HEIGHT * scale)
        plate_zoomed = plate_base.resize((w_curr, h_curr), Image.Resampling.LANCZOS)
        crop_x = (w_curr - WIDTH) // 2
        crop_y = (h_curr - HEIGHT) // 2
        canvas = plate_zoomed.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT)).copy()
        
        # Logo 居中偏上
        logo_x = (WIDTH - logo_w) // 2
        logo_y = int(HEIGHT * 0.36)
        canvas.paste(logo_scaled, (logo_x, logo_y), logo_scaled)
        
        draw = ImageDraw.Draw(canvas)
        
        # 標語：給心上弦，重新出發。
        slogan_text = "給心上弦，重新出發。"
        slogan_bbox = draw.textbbox((0, 0), slogan_text, font=font_slogan)
        slogan_w = slogan_bbox[2] - slogan_bbox[0]
        slogan_x = (WIDTH - slogan_w) // 2
        slogan_y = int(HEIGHT * 0.60)
        
        # 陰影 + 字
        draw.text((slogan_x + 3, slogan_y + 3), slogan_text, font=font_slogan, fill=(20, 15, 30, 200))
        draw.text((slogan_x, slogan_y), slogan_text, font=font_slogan, fill=(255, 253, 248, 255))
        
        # 底部標註：開發中畫面 · 官網搶先看
        sub_text = "開發中畫面 · 官網搶先看"
        sub_bbox = draw.textbbox((0, 0), sub_text, font=font_sub)
        sub_w = sub_bbox[2] - sub_bbox[0]
        sub_x = (WIDTH - sub_w) // 2
        sub_y = int(HEIGHT * 0.88)
        
        draw.text((sub_x + 2, sub_y + 2), sub_text, font=font_sub, fill=(10, 10, 15, 200))
        draw.text((sub_x, sub_y), sub_text, font=font_sub, fill=(210, 215, 220, 220))
        
        frame_idx = start_frame + i
        out_f = os.path.join(OUT_DIR, f"frame_{frame_idx:04d}.png")
        if os.path.exists(out_f) and os.path.getsize(out_f) > 1000:
            continue
        canvas.convert("RGB").save(out_f)

def build_audio():
    print(">>> Generating Composite Audio Track (18.0s AAC)...")
    audio_out = os.path.join(ROOT, "proofs/render_18s/audio_18s.aac")
    
    # 時間軸點：
    # 0.0s: clock.wav
    # 3.2s: slash.wav
    # 4.2s: hit.wav
    # 5.8s: clash.wav
    # 6.8s: hit.wav
    # 8.3s: fire.wav
    # 9.3s: break.wav
    # 10.8s: rock.wav
    # 11.9s: break.wav
    # 13.2s: wind.wav
    # 13.8s: slash.wav
    # 14.5s: hit.wav
    # 15.8s: clock.wav
    
    sfx = lambda name: os.path.join(ROOT, f"game/assets/audio/sfx/{name}.wav")
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo:d=18.0",
        "-i", sfx("clock"),  # 1
        "-i", sfx("slash"),  # 2
        "-i", sfx("hit"),    # 3
        "-i", sfx("clash"),  # 4
        "-i", sfx("fire"),   # 5
        "-i", sfx("break"),  # 6
        "-i", sfx("rock"),   # 7
        "-i", sfx("wind"),   # 8
        "-filter_complex",
        "[1:a]adelay=0|0[a0];"
        "[2:a]adelay=3200|3200[a1];"
        "[3:a]adelay=4200|4200[a2];"
        "[4:a]adelay=5800|5800[a3];"
        "[3:a]adelay=6800|6800[a4];"
        "[5:a]adelay=8300|8300[a5];"
        "[6:a]adelay=9300|9300[a6];"
        "[7:a]adelay=10800|10800[a7];"
        "[6:a]adelay=11900|11900[a8];"
        "[8:a]adelay=13200|13200[a9];"
        "[2:a]adelay=13800|13800[a10];"
        "[3:a]adelay=14500|14500[a11];"
        "[1:a]adelay=15800|15800[a12];"
        "[0:a][a0][a1][a2][a3][a4][a5][a6][a7][a8][a9][a10][a11][a12]amix=inputs=14:normalize=0:duration=first[outa]",
        "-map", "[outa]",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        audio_out
    ]
    subprocess.run(cmd, check=True)
    print("  --> Audio saved:", audio_out)
    return audio_out

def build_final_video(audio_path):
    print(">>> Assembling Final Video (mk_shorts_five_races_combat_18s.mp4)...")
    out_mp4 = os.path.join(ROOT, "web/media/shorts/mk_shorts_five_races_combat_18s.mp4")
    os.makedirs(os.path.dirname(out_mp4), exist_ok=True)
    
    cmd = [
        "ffmpeg", "-y",
        "-framerate", "30",
        "-i", os.path.join(OUT_DIR, "frame_%04d.png"),
        "-i", audio_path,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "19",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", "18.00",
        out_mp4
    ]
    subprocess.run(cmd, check=True)
    print("  --> Video successfully exported:", out_mp4)
    return out_mp4

def generate_contact_sheet(video_path):
    print(">>> Generating 6-Frame Contact Sheet...")
    sheet_path = os.path.join(ROOT, "docs/marketing/shots/mk_shorts_five_races_combat_18s_contact_sheet.png")
    os.makedirs(os.path.dirname(sheet_path), exist_ok=True)
    
    # 6 幀抽樣：
    # 1. Shot 1 (t=1.5s): 懸念開場發條特寫
    # 2. Shot 2 (t=4.2s): 兔族白金兔晨光長劍命中
    # 3. Shot 3 (t=6.8s): 獅族烈鬃獅皇家長槍突貫
    # 4. Shot 4 (t=9.3s): 狐族靈尾狐秘術法杖爆裂
    # 5. Shot 5 (t=11.8s): 豬族鋼牙豕重型戰鎚砸地
    # 6. Shot 6 (t=14.5s): 猴族靈爪猴機關靈爪狂暴連擊
    # 7. Shot 7 (t=16.8s): 官方字標點題收束
    # 做 6 格：Shot 1 (1.5s), 兔 (4.2s), 獅 (6.8s), 狐 (9.3s), 豬 (11.8s), 猴 (14.5s), 點題 (16.8s) -> 7 格拼貼 4x2 或 3x2
    # 任務要求：「附 contact sheet 抽格（至少 6 格，含五族各一＋標題鏡）」
    # 我們做 7 格完整拼貼（包含 Shot 1 到 Shot 7 全部）！
    
    sample_times = [
        ("Shot 1 微距懸念", 1.5),
        ("Shot 2 兔族晨光長劍", 4.2),
        ("Shot 3 獅族皇家長槍", 6.8),
        ("Shot 4 狐族秘術法杖", 9.3),
        ("Shot 5 豬族鍛爐重鎚", 11.8),
        ("Shot 6 猴族靈爪暴怒", 14.5),
        ("Shot 7 點題官方字標", 16.8),
    ]
    
    tmp_dir = "/tmp/contact_sheet_samples"
    os.makedirs(tmp_dir, exist_ok=True)
    
    sample_imgs = []
    for label, sec in sample_times:
        p = os.path.join(tmp_dir, f"sample_{sec:.1f}.png")
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error",
            "-ss", f"{sec:.2f}",
            "-i", video_path,
            "-vframes", "1",
            p
        ], check=True)
        img = Image.open(p).convert("RGBA")
        sample_imgs.append((label, img))
    
    # 拼貼成一張 4 欄或 7 欄大圖，每個圖寬 360，高 640
    thumb_w = 360
    thumb_h = 640
    pad = 20
    header_h = 70
    
    cols = 4
    rows = 2
    canvas_w = cols * thumb_w + (cols + 1) * pad
    canvas_h = rows * thumb_h + (rows + 1) * pad + header_h
    
    sheet = Image.new("RGBA", (canvas_w, canvas_h), (25, 23, 33, 255))
    draw = ImageDraw.Draw(sheet)
    font_title = ImageFont.truetype(FONT_PATH, 32)
    font_label = ImageFont.truetype(FONT_PATH, 22)
    
    draw.text((pad, 20), "《發條之心》18 秒五族實機打擊短影音分鏡抽樣查驗 (mk_shorts_five_races_combat_18s)", font=font_title, fill=(255, 215, 60, 255))
    
    for idx, (label, img) in enumerate(sample_imgs):
        c = idx % cols
        r = idx // cols
        x = pad + c * (thumb_w + pad)
        y = header_h + pad + r * (thumb_h + pad)
        
        resized = img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(resized, (x, y))
        
        # 標籤底條
        draw.rectangle([x, y + thumb_h - 40, x + thumb_w, y + thumb_h], fill=(0, 0, 0, 190))
        draw.text((x + 10, y + thumb_h - 35), label, font=font_label, fill=(255, 255, 255, 255))
    
    sheet.convert("RGB").save(sheet_path)
    print("  --> Contact sheet saved:", sheet_path)
    return sheet_path

def main():
    render_shot1()
    render_combat_shot("rabbit", 90, 1.10)
    render_combat_shot("lion", 165, 1.12)
    render_combat_shot("fox", 240, 1.15)
    render_combat_shot("boar", 315, 1.18, pan_y=0.2)
    render_combat_shot("macaque", 390, 1.20)
    render_shot7(465)
    
    audio_path = build_audio()
    video_path = build_final_video(audio_path)
    sheet_path = generate_contact_sheet(video_path)
    print(">>> ALL RENDER TASKS COMPLETED!")

if __name__ == "__main__":
    main()
