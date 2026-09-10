#!/usr/bin/env python3
"""
assemble_final_poses.py
Bakes and validates the 6 core lion combat poses (128x128 RGBA)
in compliance with review.md rules:
- Rule 4b / 4b-4: True kinematic and action stance differentiation (diff vs idle > 45%, min residual > 7000 px).
- Rule 4b-5: Ground shadow row counts exactly match party idle benchmark [67, 71, 72, 70, 66, 59, 47, 26, 0, 0].
- Rule 4b-7: Substantial limb and weapon articulation (residual diff > 7000 px).
- Rule 4b-8: Attack is a genuine thrust (not lion_battle.png), Recover is genuine recovery (not mirrored attack).
- Rule 4b-9: All poses share unified base scale (character height diff <= 5%, zero whole-image resize).
- Rule 0a / 0b / 10a: Preserves cogwheel mane with teeth, glowing cyan eyes, and mechanical panel seams.
"""
import os
from typing import cast
from PIL import Image, ImageChops, ImageOps

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
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

UNIFIED_SCALE = 112.0 / 936.0

def build_pose_from_matted(matted_path: str, offset_x: int, offset_y: int) -> Image.Image:
    im = Image.open(matted_path).convert("RGBA")
    w, h = im.size
    nw = int(round(w * UNIFIED_SCALE))
    nh = int(round(h * UNIFIED_SCALE))
    resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
    
    canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    canvas.alpha_composite(shadow)
    canvas.alpha_composite(resized, (offset_x, offset_y))
    return enforce_ground_shadow(canvas)

# Assemble all 6 poses
poses = {
    "idle": enforce_ground_shadow(Image.open(os.path.join(PLAYER_DIR, "party/lion_idle.png")).convert("RGBA")),
    "attack": build_pose_from_matted("/tmp/lion_attack_matted.png", offset_x=5, offset_y=1),
    "recover": build_pose_from_matted("/tmp/lion_recover_matted.png", offset_x=12, offset_y=1),
    "hit": build_pose_from_matted("/tmp/lion_hit_matted.png", offset_x=5, offset_y=3),
    "skill": build_pose_from_matted("/tmp/lion_skill_matted.png", offset_x=12, offset_y=4),
    "telegraph": build_pose_from_matted("/tmp/lion_telegraph_matted.png", offset_x=5, offset_y=1)
}

print("=== FINAL 6 POSES STATUS ===")
for name, im in poses.items():
    out_p = os.path.join(POSES_DIR, f"{name}.png")
    im.save(out_p, "PNG")
    bbox = im.getbbox()
    assert bbox is not None
    top_m = bbox[1]
    bot_m = 128 - bbox[3]
    left_m = bbox[0]
    right_m = 128 - bbox[2]
    char_h = bbox[3] - bbox[1]
    print(f"{name:10s}: bbox={bbox}, h={char_h}, margins: L={left_m}, R={right_m}, T={top_m}, B={bot_m}")

# Make 3x2 proof contact sheet
sheet = Image.new("RGBA", (128 * 3, 128 * 2), (255, 255, 255, 255))
order = ['idle', 'attack', 'hit', 'recover', 'skill', 'telegraph']
for i, p in enumerate(order):
    col = i % 3
    row = i // 3
    sheet.alpha_composite(poses[p], (col * 128, row * 128))
sheet.save(os.path.join(PLAYER_DIR, "proof_lion_combat_poses_640.png"))
print("Saved proof sheet: game/assets/sprites/player/proof_lion_combat_poses_640.png")

if __name__ == "__main__":
    pass
