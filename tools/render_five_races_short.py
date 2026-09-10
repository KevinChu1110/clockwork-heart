#!/usr/bin/env python3
import os
import math
import shutil
import subprocess
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageEnhance

ROOT = os.environ.get("GAME_ROOT", os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
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
    # crop=222:396:455:372 (微距無文字區)
    crop_x = 455
    crop_y = 372
    crop_w = 222
    crop_h = 396
    
    for i in range(90):
        out_f = os.path.join(OUT_DIR, f"frame_{i:04d}.png")
        if os.path.exists(out_f) and os.path.getsize(out_f) > 1000:
            continue
            
        t = i / 89.0
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
            
        frame_scaled.convert("RGB").save(out_f)

def render_combat_shot(race, start_frame, max_zoom, pan_y=0.0):
    rdir = os.path.join(FRAMES_BASE, race)
    print(f">>> Rendering Combat Shot: {race} (frames {start_frame} - {start_frame + 74})...")
    
    for i in range(75):
        frame_idx = start_frame + i
        out_f = os.path.join(OUT_DIR, f"frame_{frame_idx:04d}.png")
        if os.path.exists(out_f) and os.path.getsize(out_f) > 1000:
            continue
            
        raw_path = os.path.join(rdir, f"frame_{i:04d}.png")
        raw_img = Image.open(raw_path).convert("RGBA")
        
        # 1. 底層高斯模糊背景 (優化為 1/4 尺寸模糊後插值，40x 加速且視覺平滑)
        sm_w = WIDTH // 4
        sm_h = HEIGHT // 4
        bg_scale = max(sm_w / 1280.0, sm_h / 720.0)
        bw = int(1280 * bg_scale)
        bh = int(720 * bg_scale)
        sm_bg = raw_img.resize((bw, bh), Image.Resampling.BILINEAR)
        bx = (bw - sm_w) // 2
        by = (bh - sm_h) // 2
        sm_bg = sm_bg.crop((bx, by, bx + sm_w, by + sm_h))
        sm_bg = sm_bg.filter(ImageFilter.GaussianBlur(radius=8))
        bg = sm_bg.resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR)
        
        # 壓暗底層，增加對比
        darkener = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 80))
        bg = Image.alpha_composite(bg, darkener)
        
        # 2. 中央戰鬥主畫面配合推鏡
        t = i / 74.0
        scale = 1.00 + (max_zoom - 1.00) * t
        
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
        
        # 在第一幀有輕微光芒轉場 (接 Shot 1 白閃)
        if i < 4 and race == "rabbit":
            white_alpha = (4 - i) / 4.0 * 0.5
            white = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, int(255 * white_alpha)))
            bg = Image.alpha_composite(bg, white)
            
        bg.convert("RGB").save(out_f)

def render_shot7(start_frame):
    print(f">>> Rendering Shot 7: CTA End Plate with Cinematic Push-in & Shimmer (frames {start_frame} - {start_frame + 74})...")
    plate_raw = Image.open(TITLE_PLATE_PATH).convert("RGBA")
    plate_base = plate_raw.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    
    logo_raw = Image.open(LOGO_PATH).convert("RGBA")
    logo_w = int(WIDTH * 0.78)
    logo_h = int(logo_w * 640 / 1024)
    logo_base = logo_raw.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
    
    font_slogan = ImageFont.truetype(FONT_PATH, 42)
    font_sub = ImageFont.truetype(FONT_PATH, 28)
    
    for i in range(75):
        frame_idx = start_frame + i
        out_f = os.path.join(OUT_DIR, f"frame_{frame_idx:04d}.png")
        if os.path.exists(out_f) and os.path.getsize(out_f) > 1000:
            continue
            
        t = i / 74.0
        # 8% Continuous Cinematic Push-in
        scale = 1.00 + 0.08 * t
        w_curr = int(WIDTH * scale)
        h_curr = int(HEIGHT * scale)
        plate_zoomed = plate_base.resize((w_curr, h_curr), Image.Resampling.LANCZOS)
        crop_x = (w_curr - WIDTH) // 2
        crop_y = (h_curr - HEIGHT) // 2
        canvas = plate_zoomed.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT)).copy()
        
        # Logo 隨鏡頭等比微幅推進
        lw_curr = int(logo_w * scale)
        lh_curr = int(logo_h * scale)
        logo_zoomed = logo_base.resize((lw_curr, lh_curr), Image.Resampling.LANCZOS)
        
        # 標誌光暈呼吸微動 (解決相鄰幀差僅 0.22 的靜止問題)
        breath = 0.92 + 0.12 * math.sin(t * math.pi * 3.0)
        enhancer = ImageEnhance.Brightness(logo_zoomed)
        logo_active = enhancer.enhance(breath)
        
        logo_x = (WIDTH - lw_curr) // 2
        logo_y = int(HEIGHT * 0.36 - (lh_curr - logo_h) * 0.5)
        canvas.paste(logo_active, (logo_x, logo_y), logo_active)
        
        # 金色流光橫掠 (Golden light sweep across logo)
        sweep_cx = int(-150 + (WIDTH + 300) * t)
        shimmer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(shimmer)
        for sx in range(sweep_cx - 80, sweep_cx + 80):
            if 0 <= sx < WIDTH:
                dist = abs(sx - sweep_cx) / 80.0
                alpha = int(45 * (1.0 - dist) * (1.0 - dist))
                sdraw.line([(sx, logo_y), (sx + 40, logo_y + lh_curr)], fill=(255, 230, 140, alpha), width=1)
        canvas = Image.alpha_composite(canvas, shimmer)
        
        draw = ImageDraw.Draw(canvas)
        
        # 標語：給心上弦，重新出發。
        slogan_text = "給心上弦，重新出發。"
        slogan_bbox = draw.textbbox((0, 0), slogan_text, font=font_slogan)
        slogan_w = slogan_bbox[2] - slogan_bbox[0]
        slogan_x = (WIDTH - slogan_w) // 2
        slogan_y = int(HEIGHT * 0.60 - 5 * t)
        
        # 陰影 + 奶白字
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
        
        canvas.convert("RGB").save(out_f)

def build_audio():
    print(">>> Generating Composite Audio Track (18.0s AAC)...")
    audio_out = os.path.join(ROOT, "proofs/render_18s/audio_18s.aac")
    os.makedirs(os.path.dirname(audio_out), exist_ok=True)
    
    # 時間軸點：
    # 0.0s: clock.wav (發條咬合)
    # 3.2s: slash.wav (長劍破空)
    # 4.2s: hit.wav (長劍命中)
    # 5.8s: clash.wav (長槍交鋒)
    # 6.8s: hit.wav (長槍穿透)
    # 8.3s: fire.wav (秘術引導)
    # 9.4s: break.wav (法杖爆裂)
    # 10.8s: rock.wav (戰鎚破空)
    # 11.8s: break.wav (戰鎚砸地)
    # 13.2s: wind.wav (彈簧伸縮)
    # 13.8s: slash.wav (靈爪撕裂)
    # 14.4s: hit.wav (靈爪暴擊)
    # 15.8s: clock.wav (終局喀嗒)
    
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
        "[6:a]adelay=9400|9400[a6];"
        "[7:a]adelay=10800|10800[a7];"
        "[6:a]adelay=11800|11800[a8];"
        "[8:a]adelay=13200|13200[a9];"
        "[2:a]adelay=13800|13800[a10];"
        "[3:a]adelay=14400|14400[a11];"
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
    print(">>> Generating 7-Frame Contact Sheet and Individual Frame Proofs...")
    sheet_path = os.path.join(ROOT, "docs/marketing/shots/mk_shorts_five_races_combat_18s_contact_sheet.png")
    shots_dir = os.path.join(ROOT, "docs/marketing/shots")
    os.makedirs(shots_dir, exist_ok=True)
    
    # 7 幀精確抽格（依據審查意見：標籤與畫面實際內容 100% 一致，標明第幾格）：
    # 1. Shot 1 (1.50s, f0045): 微距懸念發條特寫
    # 2. Shot 2 (4.20s, f0126): 兔族晨光長劍命中 (紅字85+受擊特效)
    # 3. Shot 3 (6.80s, f0204): 獅族皇家長槍突貫 (紅字75+槍尖穿透)
    # 4. Shot 4 (9.40s, f0282): 狐族秘術法杖爆裂 (紅字62+光環爆裂)
    # 5. Shot 5 (11.80s, f0354): 豬族鍛爐重鎚砸地 (紅字61+轟擊特效)
    # 6. Shot 6 (14.433s, f0433): 猴族機關靈爪連擊 (暴擊169!+利爪抓擊)
    # 7. Shot 7 (16.80s, f0504): 官方字標推進點題 (8%推進+流光呼吸)
    sample_items = [
        ("Shot 1 微距懸念發條 (f0045, 1.5s)", 1.500, "proof_f0045_shot1_macro.png"),
        ("Shot 2 兔族晨光長劍命中 (f0126, 4.2s)", 4.200, "proof_f0126_rabbit_dawn_blade.png"),
        ("Shot 3 獅族皇家長槍突貫 (f0204, 6.8s)", 6.800, "proof_f0204_lion_knight_pike.png"),
        ("Shot 4 狐族秘術法杖爆裂 (f0282, 9.4s)", 9.400, "proof_f0282_fox_star_rod.png"),
        ("Shot 5 豬族鍛爐重鎚砸地 (f0354, 11.8s)", 11.800, "proof_f0354_boar_anvil_hammer.png"),
        ("Shot 6 猴族機關靈爪連擊 (f0433, 14.4s)", 14.433, "proof_f0433_macaque_hunt_claw.png"),
        ("Shot 7 官方字標推進點題 (f0504, 16.8s)", 16.800, "proof_f0504_shot7_title.png"),
    ]
    
    sample_imgs = []
    for label, sec, proof_fname in sample_items:
        proof_path = os.path.join(shots_dir, proof_fname)
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error",
            "-ss", f"{sec:.3f}",
            "-i", video_path,
            "-vframes", "1",
            proof_path
        ], check=True)
        img = Image.open(proof_path).convert("RGBA")
        sample_imgs.append((label, img))
        print(f"  --> Extracted individual proof: {proof_path}")
    
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
    font_label = ImageFont.truetype(FONT_PATH, 20)
    
    draw.text((pad, 20), "《發條之心》18 秒五族實機打擊短影音分鏡抽樣查驗 (mk_shorts_five_races_combat_18s)", font=font_title, fill=(255, 215, 60, 255))
    
    for idx, (label, img) in enumerate(sample_imgs):
        c = idx % cols
        r = idx // cols
        x = pad + c * (thumb_w + pad)
        y = header_h + pad + r * (thumb_h + pad)
        
        resized = img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(resized, (x, y))
        
        # 標籤底條
        draw.rectangle([x, y + thumb_h - 44, x + thumb_w, y + thumb_h], fill=(0, 0, 0, 205))
        draw.text((x + 8, y + thumb_h - 36), label, font=font_label, fill=(255, 255, 255, 255))
    
    sheet.convert("RGB").save(sheet_path)
    print("  --> Contact sheet saved:", sheet_path)
    return sheet_path

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    
    render_shot1()                                      # frames 0..89 (0.0s - 3.0s)
    render_combat_shot("rabbit", 90, 1.10)              # frames 90..164 (3.0s - 5.5s)
    render_combat_shot("lion", 165, 1.12)               # frames 165..239 (5.5s - 8.0s)
    render_combat_shot("fox", 240, 1.15)                # frames 240..314 (8.0s - 10.5s)
    render_combat_shot("boar", 315, 1.18, pan_y=0.2)   # frames 315..389 (10.5s - 13.0s)
    render_combat_shot("macaque", 390, 1.20)            # frames 390..464 (13.0s - 15.5s)
    render_shot7(465)                                   # frames 465..539 (15.5s - 18.0s)
    
    audio_path = build_audio()
    video_path = build_final_video(audio_path)
    sheet_path = generate_contact_sheet(video_path)
    print(">>> ALL RENDER TASKS COMPLETED!")

if __name__ == "__main__":
    main()
