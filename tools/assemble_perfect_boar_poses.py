#!/usr/bin/env python3
"""
tools/assemble_perfect_boar_poses.py
Assembles all 6 final Boar combat action poses into game/assets/sprites/player/poses/boar/:
- idle: party/boar_idle.png (with tan dirt patch stripped, pure clean soft charcoal shadow)
- telegraph: /tmp/full_pose_telegraph_clean.png
- attack: layered composite with rigid hammer assembly shifted dx=32 to fit inside canvas (x=124..127 strictly 0)
- recover: /tmp/recover_clean_intact.png tilted -4 deg for aggressive forward-impact recovery squat
- skill: /tmp/skill_full_intact.png (cleaned stray specks, full hammer & aura)
- hit: /tmp/hit_clean_intact.png (top 10 rows trimmed to eliminate stray white sliver)
All 128x128 RGBA, Rule 4b-5 compliant soft translucent charcoal ground shadow.
"""

import os
from typing import cast
from PIL import Image, ImageChops, ImageDraw, ImageFilter

REPO_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_9c7dae2a"
PARTY_IDLE = f"{REPO_ROOT}/game/assets/sprites/player/party/boar_idle.png"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/boar"

W, H = 128, 128

def build_clean_contact_shadow(cx: int = 64, cy: int = 120, rx: int = 42, ry: int = 6, blur: float = 0.7) -> Image.Image:
    shadow_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow_canvas)
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(40, 30, 45, 130))
    draw.ellipse([cx - int(rx * 0.8), cy - int(ry * 0.8), cx + int(rx * 0.8), cy + int(ry * 0.8)], fill=(40, 30, 45, 175))
    draw.ellipse([cx - int(rx * 0.55), cy - int(ry * 0.6), cx + int(rx * 0.55), cy + int(ry * 0.6)], fill=(40, 30, 45, 220))
    return shadow_canvas.filter(ImageFilter.GaussianBlur(blur))

shadow_standard = build_clean_contact_shadow(cx=64, cy=120, rx=42, ry=6, blur=0.7)

def remove_stray_specks(im: Image.Image, min_size: int = 30) -> Image.Image:
    w, h = im.size
    px = im.load()
    assert px is not None
    visited = [[False for _ in range(w)] for _ in range(h)]
    out = im.copy()
    o_px = out.load()
    assert o_px is not None

    for y in range(h):
        for x in range(w):
            if cast(tuple[int, ...], px[x, y])[3] > 30 and not visited[y][x]:
                comp = [(x, y)]
                visited[y][x] = True
                q = [(x, y)]
                while q:
                    cx, cy = q.pop(0)
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < w and 0 <= ny < h:
                            if cast(tuple[int, ...], px[nx, ny])[3] > 30 and not visited[ny][nx]:
                                visited[ny][nx] = True
                                q.append((nx, ny))
                                comp.append((nx, ny))
                if len(comp) < min_size:
                    for px_x, px_y in comp:
                        o_px[px_x, px_y] = (0, 0, 0, 0)
    return out

def strip_tan_and_shadow(im: Image.Image) -> Image.Image:
    """Removes the AI tan dirt patch / baked-in shadows from the bottom of the raw character sprite."""
    w, h = im.size
    out = im.copy()
    px = out.load()
    assert px is not None
    for y in range(int(h * 0.82), h):
        for x in range(w):
            p = cast(tuple[int, ...], px[x, y])
            if p[3] > 0:
                r, g, b = p[0], p[1], p[2]
                is_tan = (r > 125 and g > 105 and b > 75) or (p[3] < 120 and y > h * 0.88)
                is_dark_foot = (p[3] > 200 and r < 110 and g < 95 and b < 85)
                if is_tan and not is_dark_foot:
                    px[x, y] = (0, 0, 0, 0)
    return out

def enforce_ground_shadow(img: Image.Image) -> Image.Image:
    out = img.copy()
    sh_px = shadow_standard.load()
    o_px = out.load()
    assert sh_px is not None and o_px is not None
    for y in range(118, 128):
        for x in range(W):
            sp = cast(tuple[int, int, int, int], sh_px[x, y])
            op = cast(tuple[int, int, int, int], o_px[x, y])
            if sp[3] == 0:
                o_px[x, y] = (0, 0, 0, 0)
            elif op[3] > 0 and (op[0] > 125 and op[1] > 105 and op[2] > 75):
                o_px[x, y] = sp
    return out

def format_pose(raw_path: str, target_h: int, offset_y: int, offset_x: int = -1, trim_top: int = 0) -> Image.Image:
    raw = Image.open(raw_path).convert("RGBA")
    if trim_top > 0:
        rw, rh = raw.size
        raw = raw.crop((0, trim_top, rw, rh))
    cleaned = strip_tan_and_shadow(raw)
    cleaned = remove_stray_specks(cleaned, min_size=35)
    bbox = cleaned.getbbox()
    assert bbox is not None
    tight = cleaned.crop(bbox)
    tw, th = tight.size
    scale = target_h / float(th)
    target_w = int(round(tw * scale))
    resized = tight.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    if offset_x == -1:
        offset_x = max(2, (W - target_w) // 2)

    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.alpha_composite(shadow_standard)
    canvas.alpha_composite(resized, (offset_x, offset_y))
    return enforce_ground_shadow(canvas)

# 1. Idle: strip the old tan dirt platform and use canonical clean shadow
base_idle = Image.open(PARTY_IDLE).convert("RGBA")
idle_body = strip_tan_and_shadow(base_idle)
idle_im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
idle_im.alpha_composite(shadow_standard)
idle_im.alpha_composite(idle_body)
idle_im = enforce_ground_shadow(idle_im)

# 2. Telegraph: wind-up charge
telegraph_im = format_pose("/tmp/full_pose_telegraph_clean.png", target_h=114, offset_y=11, offset_x=14)

# 3. Attack: massive downward slam impact with rigid hammer shifted inward
def build_perfect_attack_pose() -> Image.Image:
    raw = Image.open("/tmp/preview_raw_atk.png").convert("RGBA")
    w, h = raw.size

    # Layer 1: Body (head, tusks, snout, ears, crest, winding key, body, legs, hands)
    body_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    b_px = body_layer.load()
    r_px = raw.load()
    assert b_px is not None and r_px is not None

    for y in range(h):
        for x in range(w):
            p = cast(tuple[int, ...], r_px[x, y])
            if p[3] == 0:
                continue
            if y > 275 and (p[0] > 125 and p[1] > 105 and p[2] > 75):
                continue
            if y < 165 and x <= 285:
                b_px[x, y] = p
            elif y >= 165 and x <= 255:
                b_px[x, y] = p

    # Layer 2: Hammer (shaft connection, metal sleeve, stone hammer block, right metal hub/cap)
    hammer_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    h_px = hammer_layer.load()
    assert h_px is not None

    for y in range(160, 276):
        for x in range(265, 378):
            p = cast(tuple[int, ...], r_px[x, y])
            if p[3] > 30:
                if y > 262 and (p[0] > 125 and p[1] > 105 and p[2] > 75):
                    continue
                h_px[x, y] = p

    # Composite with dx = 32
    dx = 32
    composed = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    h_crop = hammer_layer.crop((265, 0, 378, h))
    composed.paste(h_crop, (265 - dx, 0), h_crop)
    composed.paste(body_layer, (0, 0), body_layer)

    bbox = composed.getbbox()
    assert bbox is not None
    tight = composed.crop(bbox)
    tw, th = tight.size

    target_h = 102
    scale = target_h / float(th)
    target_w = int(round(tw * scale))
    resized = tight.resize((target_w, target_h), Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.alpha_composite(shadow_standard)
    canvas.alpha_composite(resized, (2, 22))
    return enforce_ground_shadow(canvas)

attack_im = build_perfect_attack_pose()

# 4. Recover: deep recovery crouch tilted forward (-4 deg) for aggressive impact-absorbing squat
def build_tilted_recover_pose() -> Image.Image:
    rec_raw = Image.open("/tmp/recover_clean_intact.png").convert("RGBA")
    rw, rh = rec_raw.size
    rot = rec_raw.rotate(-4, resample=Image.Resampling.BICUBIC, center=(int(rw * 0.45), int(rh * 0.95)))
    bbox = rot.getbbox()
    assert bbox is not None
    tight = rot.crop(bbox)
    tw, th = tight.size

    target_h = 98
    scale = target_h / float(th)
    target_w = int(round(tw * scale))
    resized = tight.resize((target_w, target_h), Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.alpha_composite(shadow_standard)
    canvas.alpha_composite(resized, (24, 27))
    return enforce_ground_shadow(canvas)

recover_im = build_tilted_recover_pose()

# 5. Skill: FULL 315x486 size, hammer completely intact with aura, zero stray specks!
skill_im = format_pose("/tmp/skill_full_intact.png", target_h=121, offset_y=3, offset_x=-1)

# 6. Hit: clean whiplash knockback recoil, trimmed top 12px to eliminate stray white artifact
hit_im = format_pose("/tmp/hit_clean_intact.png", target_h=104, offset_y=19, offset_x=-1, trim_top=12)

poses = {
    "idle": idle_im,
    "telegraph": telegraph_im,
    "attack": attack_im,
    "recover": recover_im,
    "skill": skill_im,
    "hit": hit_im,
}

os.makedirs(OUT_DIR, exist_ok=True)
print("=== FINAL 6 POSES STATUS ===")
for name, im in poses.items():
    out_p = os.path.join(OUT_DIR, f"{name}.png")
    im.save(out_p, "PNG")

    diff = ImageChops.difference(idle_im, im)
    diff_l = diff.convert("L")
    diff_px = sum(1 for y in range(H) for x in range(W) if cast(int, diff_l.getpixel((x, y))) > 10)
    pct = (diff_px / float(W * H)) * 100

    bbox = im.getbbox()
    print(f"[{name.upper():9s}] Saved {out_p}")
    print(f"  bbox={bbox} | diff_vs_idle={diff_px} px ({pct:.1f}%)")
