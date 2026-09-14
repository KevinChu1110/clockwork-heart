#!/usr/bin/env python3
import os
import sys
import subprocess
import wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKTREE = REPO_ROOT
OUT_DIR = os.path.join(WORKTREE, "proofs/s8_loop_clip")
S8_DIR = os.path.join(WORKTREE, "proofs/standard_scene_s8")
BRANDING_DIR = os.path.join(WORKTREE, "branding")
SFX_DIR = os.path.join(WORKTREE, "game/assets/audio/sfx")
BGM_DIR = os.path.join(WORKTREE, "game/assets/audio/bgm")
FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

WIDTH = 1280
HEIGHT = 720
FPS = 30
TOTAL_FRAMES = 540 # 18.00 seconds exactly

os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load source images
print("=== [1/5] 載入來源實機資產 ===")
shot_01 = Image.open(os.path.join(S8_DIR, "shot_01.png")).convert("RGB")
shot_02 = Image.open(os.path.join(S8_DIR, "shot_02.png")).convert("RGB")
shot_03 = Image.open(os.path.join(S8_DIR, "shot_03.png")).convert("RGB")
shot_04_step1 = Image.open(os.path.join(S8_DIR, "shot_04_step1_flash.png")).convert("RGB")
shot_04_step2 = Image.open(os.path.join(S8_DIR, "shot_04_step2_crack.png")).convert("RGB")
shot_04_step3 = Image.open(os.path.join(S8_DIR, "shot_04_step3_debris.png")).convert("RGB")
shot_04_step4 = Image.open(os.path.join(S8_DIR, "shot_04_step4_loot.png")).convert("RGB")
shot_05 = Image.open(os.path.join(S8_DIR, "shot_05.png")).convert("RGB")
logo_im = Image.open(os.path.join(BRANDING_DIR, "logo_cn_black.png")).convert("RGB")

print("所有實機圖檔載入完畢！")

def render_camera_frame(im, scale, focus_x, focus_y, out_w=WIDTH, out_h=HEIGHT, shake_x=0, shake_y=0):
    crop_w = out_w / scale
    crop_h = out_h / scale
    fx = focus_x + shake_x
    fy = focus_y + shake_y
    left = fx - crop_w / 2.0
    top = fy - crop_h / 2.0
    left = max(0.0, min(out_w - crop_w, left))
    top = max(0.0, min(out_h - crop_h, top))
    crop_box = (left, top, left + crop_w, top + crop_h)
    cropped = im.crop(crop_box)
    return cropped.resize((out_w, out_h), Image.Resampling.BILINEAR)

def render_title_card_frame(logo, t, font_path, out_w=WIDTH, out_h=HEIGHT):
    canvas = Image.new("RGB", (out_w, out_h), (8, 9, 14))
    scale = 1.00 + 0.06 * t
    lw, lh = int(880 * scale), int(550 * scale)
    scaled_logo = logo.resize((lw, lh), Image.Resampling.BILINEAR)
    
    lx = (out_w - lw) // 2
    ly = (out_h - lh) // 2 - 25
    canvas.paste(scaled_logo, (lx, ly))
    
    # Light sweep
    sweep_x = -200 + (1480 - (-200)) * t
    sweep_overlay = Image.new("RGBA", (out_w, out_h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(sweep_overlay)
    for offset in range(-80, 81):
        dist = abs(offset) / 80.0
        alpha = int(45 * (1.0 - dist * dist))
        x_pos = int(sweep_x + offset)
        s_draw.line([(x_pos, 0), (x_pos + 120, out_h)], fill=(255, 230, 160, alpha), width=1)
    
    canvas = Image.alpha_composite(canvas.convert("RGBA"), sweep_overlay).convert("RGB")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(font_path, 22)
    sub_text = "實機錄製 · 開發中畫面"
    bbox = draw.textbbox((0, 0), sub_text, font=font)
    tw = bbox[2] - bbox[0]
    tx = (out_w - tw) // 2
    ty = out_h - 65
    draw.text((tx + 1, ty + 1), sub_text, font=font, fill=(0, 0, 0))
    draw.text((tx, ty), sub_text, font=font, fill=(230, 215, 175))
    
    if t > 0.82:
        fade = (t - 0.82) / 0.18
        arr = np.array(canvas, dtype=np.float32) * (1.0 - fade)
        canvas = Image.fromarray(arr.astype(np.uint8))
    return canvas

def blend_frames(f1, f2, alpha):
    arr1 = np.array(f1, dtype=np.float32)
    arr2 = np.array(f2, dtype=np.float32)
    blended = arr1 * (1.0 - alpha) + arr2 * alpha
    return Image.fromarray(blended.astype(np.uint8))

# 2. Audio Mixing
print("=== [2/5] 多軌真實音訊合成 ===")
TARGET_RATE = 22050
NUM_SAMPLES = int(18.0 * TARGET_RATE)
left_channel = np.zeros(NUM_SAMPLES, dtype=np.float32)
right_channel = np.zeros(NUM_SAMPLES, dtype=np.float32)

def load_wav_pcm(path):
    with wave.open(path, 'rb') as w:
        n_ch = w.getnchannels()
        w_samp = w.getsampwidth()
        rate = w.getframerate()
        n_frames = w.getnframes()
        data = w.readframes(n_frames)
    if w_samp == 2:
        samples = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
    else:
        raise ValueError("Unsupported sample width")
    if n_ch == 2:
        left = samples[0::2]
        right = samples[1::2]
    else:
        left = samples
        right = samples
    if rate != TARGET_RATE:
        indices = np.linspace(0, len(left) - 1, int(len(left) * TARGET_RATE / rate))
        left = np.interp(indices, np.arange(len(left)), left)
        right = np.interp(indices, np.arange(len(right)), right)
    return left, right

def overlay_sound(dest_l, dest_r, sound_path, start_time_sec, volume=1.0, pan=0.0):
    sl, sr = load_wav_pcm(sound_path)
    start_idx = int(start_time_sec * TARGET_RATE)
    end_idx = min(len(dest_l), start_idx + len(sl))
    if start_idx >= len(dest_l):
        return
    cur_len = end_idx - start_idx
    l_vol = volume * (1.0 - max(0.0, pan))
    r_vol = volume * (1.0 + min(0.0, pan))
    dest_l[start_idx:end_idx] += sl[:cur_len] * l_vol
    dest_r[start_idx:end_idx] += sr[:cur_len] * r_vol

# Mix BGM
bgm_village_l, bgm_village_r = load_wav_pcm(os.path.join(BGM_DIR, "village.wav"))
bgm_battle_l, bgm_battle_r = load_wav_pcm(os.path.join(BGM_DIR, "battle.wav"))

# Village BGM for 0 - 3.2s
v_len = min(len(left_channel), int(3.5 * TARGET_RATE))
v_fade = int(0.5 * TARGET_RATE)
v_gain = np.ones(v_len, dtype=np.float32) * 0.25
v_gain[-v_fade:] = np.linspace(0.25, 0.0, v_fade)
left_channel[:v_len] += bgm_village_l[:v_len] * v_gain
right_channel[:v_len] += bgm_village_r[:v_len] * v_gain

# Battle BGM for 3.0s - 18.0s
b_start = int(3.0 * TARGET_RATE)
b_len = len(left_channel) - b_start
b_gain = np.ones(b_len, dtype=np.float32) * 0.32
b_fade_in = int(0.3 * TARGET_RATE)
b_fade_out = int(0.8 * TARGET_RATE)
b_gain[:b_fade_in] = np.linspace(0.0, 0.32, b_fade_in)
b_gain[-b_fade_out:] = np.linspace(0.32, 0.0, b_fade_out)
left_channel[b_start:] += bgm_battle_l[:b_len] * b_gain
right_channel[b_start:] += bgm_battle_r[:b_len] * b_gain

# Mix Sound Effects
overlay_sound(left_channel, right_channel, os.path.join(SFX_DIR, "clock.wav"), 0.15, volume=0.5)
overlay_sound(left_channel, right_channel, os.path.join(SFX_DIR, "step.wav"), 0.55, volume=0.6, pan=-0.1)
overlay_sound(left_channel, right_channel, os.path.join(SFX_DIR, "step.wav"), 1.45, volume=0.6, pan=0.1)
overlay_sound(left_channel, right_channel, os.path.join(SFX_DIR, "battle_start.wav"), 3.00, volume=0.85)
overlay_sound(left_channel, right_channel, os.path.join(SFX_DIR, "warn.wav"), 5.50, volume=0.8, pan=0.2)
overlay_sound(left_channel, right_channel, os.path.join(SFX_DIR, "slash.wav"), 6.35, volume=0.85, pan=0.1)
overlay_sound(left_channel, right_channel, os.path.join(SFX_DIR, "clash.wav"), 6.42, volume=0.75, pan=0.15)
overlay_sound(left_channel, right_channel, os.path.join(SFX_DIR, "reveal.wav"), 8.55, volume=0.8, pan=0.2)
overlay_sound(left_channel, right_channel, os.path.join(SFX_DIR, "break.wav"), 9.85, volume=0.9, pan=0.25)
overlay_sound(left_channel, right_channel, os.path.join(SFX_DIR, "wind.wav"), 11.05, volume=0.7, pan=0.3)
overlay_sound(left_channel, right_channel, os.path.join(SFX_DIR, "victory.wav"), 12.35, volume=0.75, pan=0.3)
overlay_sound(left_channel, right_channel, os.path.join(SFX_DIR, "ui.wav"), 12.50, volume=0.7, pan=0.3)
overlay_sound(left_channel, right_channel, os.path.join(SFX_DIR, "clock.wav"), 14.05, volume=0.85, pan=-0.2)
overlay_sound(left_channel, right_channel, os.path.join(SFX_DIR, "clock.wav"), 16.50, volume=0.75)

max_val = max(np.max(np.abs(left_channel)), np.max(np.abs(right_channel)))
if max_val > 0.95:
    left_channel = left_channel * (0.95 / max_val)
    right_channel = right_channel * (0.95 / max_val)

int_left = (left_channel * 32767.0).astype(np.int16)
int_right = (right_channel * 32767.0).astype(np.int16)

interleaved = np.empty((len(int_left) * 2,), dtype=np.int16)
interleaved[0::2] = int_left
interleaved[1::2] = int_right

temp_audio_path = "/tmp/s8_audio.wav"
with wave.open(temp_audio_path, 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(TARGET_RATE)
    w.writeframes(interleaved.tobytes())

print(f"音訊混合完成，輸出至 {temp_audio_path}")

# 3. Stream frames to ffmpeg via stdin
print("=== [3/5] 即時流式渲染 540 幀並串流至 ffmpeg ===")
FINAL_MP4 = os.path.join(OUT_DIR, "s8_core_loop_18s.mp4")

ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{WIDTH}x{HEIGHT}",
    "-pix_fmt", "rgb24",
    "-r", str(FPS),
    "-i", "-",
    "-i", temp_audio_path,
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    FINAL_MP4
]

proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

prev_arr = None
diff_samples = []

for f_idx in range(TOTAL_FRAMES):
    if f_idx < 90:
        t = f_idx / 89.0
        scale = 1.03 + 0.11 * t
        fx = 640.0 + 35.0 * t
        fy = 360.0 + 30.0 * t
        frame = render_camera_frame(shot_01, scale, fx, fy)
        if f_idx >= 84:
            alpha = (f_idx - 84) / 6.0
            scale2 = 1.02
            f2 = render_camera_frame(shot_02, scale2, 640, 360)
            frame = blend_frames(frame, f2, alpha)

    elif f_idx < 165:
        idx_in = f_idx - 90
        t = idx_in / 74.0
        scale = 1.02 + 0.08 * t
        fx = 640.0 - 15.0 * t
        fy = 360.0 - 10.0 * t
        frame = render_camera_frame(shot_02, scale, fx, fy)
        if f_idx >= 160:
            alpha = (f_idx - 160) / 5.0
            scale3 = 1.06
            f3 = render_camera_frame(shot_03, scale3, 680, 360)
            frame = blend_frames(frame, f3, alpha)

    elif f_idx < 255:
        idx_in = f_idx - 165
        t = idx_in / 89.0
        scale = 1.06 + 0.16 * t
        fx = 680.0 + 40.0 * t
        fy = 360.0 - 20.0 * t
        sx, sy = 0, 0
        if 192 <= f_idx <= 202:
            st = (f_idx - 192) / 10.0
            damp = 1.0 - st
            sx = int(np.sin(st * np.pi * 4) * 3.5 * damp)
            sy = int(np.cos(st * np.pi * 4) * 2.5 * damp)
        frame = render_camera_frame(shot_03, scale, fx, fy, shake_x=sx, shake_y=sy)
        if f_idx >= 250:
            alpha = (f_idx - 250) / 5.0
            f_next = render_camera_frame(shot_04_step1, 1.20, 740, 270)
            frame = blend_frames(frame, f_next, alpha)

    elif f_idx < 294:
        # S4 Step 1: 閃邊鎖定 (聚焦盾牌鎖定)
        idx_in = f_idx - 255
        t = idx_in / 38.0
        scale = 1.20 + 0.12 * t
        fx = 740.0 + 20.0 * t
        fy = 270.0 - 10.0 * t
        frame = render_camera_frame(shot_04_step1, scale, fx, fy)
        if f_idx >= 290:
            alpha = (f_idx - 290) / 4.0
            f_next = render_camera_frame(shot_04_step2, 1.40, 750, 260)
            frame = blend_frames(frame, f_next, alpha)

    elif f_idx < 330:
        # S4 Step 2: 裂縫 BREAK (純戰鬥核心特寫，避開底部白面板)
        idx_in = f_idx - 294
        t = idx_in / 35.0
        scale = 1.40 + 0.08 * t
        fx = 750.0 + 10.0 * t
        fy = 260.0
        sx, sy = 0, 0
        if idx_in < 8:
            damp = (8 - idx_in) / 8.0
            sx = int(np.sin(idx_in * 1.5) * 3.0 * damp)
            sy = int(np.cos(idx_in * 1.5) * 2.0 * damp)
        frame = render_camera_frame(shot_04_step2, scale, fx, fy, shake_x=sx, shake_y=sy)
        if f_idx >= 326:
            alpha = (f_idx - 326) / 4.0
            f_next = render_camera_frame(shot_04_step3, 1.25, 760, 270)
            frame = blend_frames(frame, f_next, alpha)

    elif f_idx < 369:
        # S4 Step 3: 零件飛出
        idx_in = f_idx - 330
        t = idx_in / 38.0
        scale = 1.25 - 0.06 * t
        fx = 760.0 + 120.0 * t
        fy = 270.0 - 50.0 * t
        frame = render_camera_frame(shot_04_step3, scale, fx, fy)
        if f_idx >= 365:
            alpha = (f_idx - 365) / 4.0
            f_next = render_camera_frame(shot_04_step4, 1.25, 920, 220)
            frame = blend_frames(frame, f_next, alpha)

    elif f_idx < 420:
        # S4 Step 4: 進欄圖示
        idx_in = f_idx - 369
        t = idx_in / 50.0
        scale = 1.25 - 0.14 * t
        fx = 920.0 - 140.0 * t
        fy = 220.0 + 60.0 * t
        frame = render_camera_frame(shot_04_step4, scale, fx, fy)
        if f_idx >= 415:
            alpha = (f_idx - 415) / 5.0
            f_next = render_camera_frame(shot_05, 1.08, 500, 380)
            frame = blend_frames(frame, f_next, alpha)

    elif f_idx < 495:
        # Shot 5: S5 收束胸口發條光＋刻度
        idx_in = f_idx - 420
        t = idx_in / 74.0
        scale = 1.08 + 0.22 * t
        fx = 500.0 - 40.0 * t
        fy = 380.0 + 15.0 * t
        frame = render_camera_frame(shot_05, scale, fx, fy)
        if f_idx >= 489:
            alpha = (f_idx - 489) / 6.0
            f_next = render_title_card_frame(logo_im, 0.0, FONT_PATH)
            frame = blend_frames(frame, f_next, alpha)

    else:
        idx_in = f_idx - 495
        t = idx_in / 44.0
        frame = render_title_card_frame(logo_im, t, FONT_PATH)

    # Frame diff tracking
    cur_arr = np.array(frame, dtype=np.float32)
    if prev_arr is not None:
        if f_idx % 10 == 0:
            diff_samples.append(np.mean(np.abs(cur_arr - prev_arr)))
    prev_arr = cur_arr

    proc.stdin.write(frame.tobytes())
    if (f_idx + 1) % 90 == 0 or f_idx == TOTAL_FRAMES - 1:
        print(f"已串流幀數: {f_idx + 1} / {TOTAL_FRAMES} ({(f_idx + 1) / FPS:.1f}s)")

proc.stdin.close()
err_out = proc.stderr.read().decode()
ret = proc.wait()

if ret != 0:
    print("ffmpeg 編碼出錯！", err_out)
    sys.exit(1)

print(f"成片 MP4 編碼完成: {FINAL_MP4}")

# Cleanup temp audio
if os.path.exists(temp_audio_path):
    os.remove(temp_audio_path)

# 4. Extract the 6 sample frames
print("=== [4/5] 抽取 6 張驗收抽格 ===")
sample_targets = [
    (0.00, "frame_00s.png"),
    (3.00, "frame_03s.png"),
    (6.00, "frame_06s.png"),
    (10.00, "frame_10s.png"),
    (14.00, "frame_14s.png"),
    (17.67, "frame_18s.png"),
]

for sec, out_name in sample_targets:
    target_path = os.path.join(OUT_DIR, out_name)
    extract_cmd = [
        "ffmpeg", "-y",
        "-ss", str(sec),
        "-i", FINAL_MP4,
        "-vframes", "1",
        "-q:v", "2",
        target_path
    ]
    sub_res = subprocess.run(extract_cmd, capture_output=True, text=True)
    if sub_res.returncode != 0:
        print(f"抽格失敗 {out_name}:", sub_res.stderr)
        sys.exit(1)
    print(f"已抽格: {out_name} @ {sec:.2f}s")

# 5. Quality metrics verification
print("=== [5/5] 執行客觀品質標準檢驗 ===")
dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", FINAL_MP4]
dur_out = subprocess.check_output(dur_cmd).decode().strip()
duration = float(dur_out)
print(f"影片時長: {duration:.3f} 秒 (規格要求: 15-20s, <=20s)")
assert 15.0 <= duration <= 20.0, "時長不合規格！"

audio_cmd = ["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=codec_name", "-of", "csv=p=0", FINAL_MP4]
audio_out = subprocess.check_output(audio_cmd).decode().strip()
print(f"音訊編碼: {audio_out} (第 14a 條檢驗)")
assert len(audio_out) > 0, "音軌為空！不合格！"

res_cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", FINAL_MP4]
res_out = subprocess.check_output(res_cmd).decode().strip()
print(f"影片解析度: {res_out} (規格要求: 1280,720)")
assert res_out == "1280,720", "解析度不符！"

mean_adj_diff = np.mean(diff_samples)
print(f"全片相鄰幀平均動態差異: {mean_adj_diff:.3f} (門檻 > 1.0)")
assert mean_adj_diff > 1.0, "動態差異過小！"

print("=== 影片產出與驗證全部成功！ ===")
