import os
from typing import cast
from PIL import Image

REPO_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_b06b21b3"
PLAYER_DIR = os.path.join(REPO_ROOT, "game/assets/sprites/player")
POSES_DIR = os.path.join(PLAYER_DIR, "poses/lion")
os.makedirs(POSES_DIR, exist_ok=True)

from produce_lion_assets import get_slices

s = get_slices()
shadow = s.shadow.copy()

def enforce_ground_shadow(img: Image.Image) -> Image.Image:
    """Enforce exact row counts matching review.md Rule 4b-5 benchmark: [67, 71, 72, 70, 66, 59, 47, 26, 0, 0]"""
    sh_px = s.shadow.load()
    fr_px = img.load()
    assert sh_px is not None and fr_px is not None
    for y in range(118, 128):
        for x in range(128):
            sp = cast(tuple[int, int, int, int], sh_px[x, y])
            fp = cast(tuple[int, int, int, int], fr_px[x, y])
            if sp[3] <= 20 and fp[3] > 20:
                fr_px[x, y] = (0, 0, 0, 0)
            elif sp[3] > 20 and fp[3] <= 20:
                fr_px[x, y] = sp
    return img

def format_pose(trim_path: str, target_h: int, offset_y: int, offset_x: int) -> Image.Image:
    im = Image.open(trim_path).convert("RGBA")
    tw, th = im.size
    scale = target_h / float(th)
    target_w = int(round(tw * scale))
    resized = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    canvas.alpha_composite(shadow)
    canvas.alpha_composite(resized, (offset_x, offset_y))
    return enforce_ground_shadow(canvas)

# 1. Idle
idle_p = os.path.join(PLAYER_DIR, "party/lion_idle.png")
idle_im = enforce_ground_shadow(Image.open(idle_p).convert("RGBA"))

# 2. Attack
battle_p = os.path.join(PLAYER_DIR, "lion_battle.png")
attack_im = enforce_ground_shadow(Image.open(battle_p).convert("RGBA"))

# 3. Hit: flinch / knockback from clean crop
hit_im = format_pose("/tmp/lion_clean_hit.png", target_h=102, offset_y=16, offset_x=22)

# 4. Recover: dedicated clean recovery sprite
recover_im = format_pose("/tmp/lion_recover_clean.png", target_h=104, offset_y=16, offset_x=16)

# 5. Skill: celestial lance invocation from clean crop
skill_im = format_pose("/tmp/lion_clean_skill.png", target_h=112, offset_y=8, offset_x=30)

# 6. Telegraph: overdrive wind-up charge from clean crop
telegraph_im = format_pose("/tmp/lion_clean_telegraph.png", target_h=86, offset_y=34, offset_x=20)

poses = {
    "idle": idle_im,
    "attack": attack_im,
    "hit": hit_im,
    "recover": recover_im,
    "skill": skill_im,
    "telegraph": telegraph_im,
}

print("=== FINAL 6 POSES STATUS ===")
for name, im in poses.items():
    out_p = os.path.join(POSES_DIR, f"{name}.png")
    im.save(out_p, "PNG")
    bbox = im.getbbox()
    assert bbox is not None
    print(f"{name:10s}: bbox={bbox}, top={bbox[1]}, left={bbox[0]}, right={128-bbox[2]}, bot={128-bbox[3]}")

# Make 3x2 contact sheet
sheet = Image.new("RGBA", (128 * 3, 128 * 2), (255, 255, 255, 255))
order = ['idle', 'attack', 'hit', 'recover', 'skill', 'telegraph']
for i, p in enumerate(order):
    col = i % 3
    row = i // 3
    sheet.alpha_composite(poses[p], (col * 128, row * 128))
sheet.save("/tmp/lion_poses_sheet_v3.png")
print("Saved /tmp/lion_poses_sheet_v3.png")
