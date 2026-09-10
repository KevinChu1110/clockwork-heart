#!/usr/bin/env python3
"""
unify_lion_heads.py
Unified head feature alignment for the 5 lion combat poses:
- Restores circular cyan optical lens eyes (20 px, 6x5 bounding box, dark socket rim) matching baseline party/lion_idle.png.
- Restores mechanical panel mold seam line and cheek plate rivets matching baseline.
- Strictly modifies only the head region (y < 60), leaving stance, limbs, lance, torso, and soft shadow untouched.
- Updates proof_lion_combat_poses_640.png and generates proof_lion_head_unification_7x.png.
"""
import os
from PIL import Image
import numpy as np

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLAYER_DIR = os.path.join(REPO_ROOT, "game/assets/sprites/player")
POSES_DIR = os.path.join(PLAYER_DIR, "poses/lion")
PARTY_IDLE = os.path.join(PLAYER_DIR, "party/lion_idle.png")

TARGET_EYE_CENTERS = {
    "telegraph": (64, 35),
    "attack":    (61, 37),
    "recover":   (70, 37),
    "skill":     (74, 39),
    "hit":       (73, 29),
}

def build_feather_mask() -> np.ndarray:
    mask = np.ones((28, 28), dtype=float)
    for i in range(28):
        for j in range(28):
            dist = min(i, 27 - i, j, 27 - j)
            if dist == 0:
                mask[i, j] = 0.0
            elif dist == 1:
                mask[i, j] = 0.5
            elif dist == 2:
                mask[i, j] = 0.85
            else:
                mask[i, j] = 1.0
    return mask

def main():
    idle_im = Image.open(PARTY_IDLE).convert("RGBA")
    idle_arr = np.array(idle_im)
    face_patch = idle_arr[27:55, 58:86].copy()
    mask = build_feather_mask()

    for name, (cx, cy) in TARGET_EYE_CENTERS.items():
        p_path = os.path.join(POSES_DIR, f"{name}.png")
        im = Image.open(p_path).convert("RGBA")
        arr = np.array(im)
        mod_arr = arr.copy()
        
        x0 = cx - 6
        y0 = cy - 16
        
        for py in range(28):
            for px in range(28):
                ty = y0 + py
                tx = x0 + px
                if 0 <= ty < 60 and 0 <= tx < 128:
                    if arr[ty, tx, 3] > 100:
                        w = mask[py, px]
                        src_rgb = face_patch[py, px, :3]
                        dst_rgb = arr[ty, tx, :3]
                        mod_arr[ty, tx, :3] = np.round(src_rgb * w + dst_rgb * (1.0 - w)).astype(np.uint8)
        
        out_im = Image.fromarray(mod_arr)
        out_im.save(p_path, "PNG")
        print(f"Unified head features in {p_path}")

    # Update proof_lion_combat_poses_640.png
    order = ['idle', 'attack', 'hit', 'recover', 'skill', 'telegraph']
    sheet = Image.new("RGBA", (128 * 3, 128 * 2), (255, 255, 255, 255))
    for i, p in enumerate(order):
        col = i % 3
        row = i // 3
        im = Image.open(os.path.join(POSES_DIR, f"{p}.png")).convert("RGBA")
        sheet.alpha_composite(im, (col * 128, row * 128))
    sheet_p = os.path.join(PLAYER_DIR, "proof_lion_combat_poses_640.png")
    sheet.save(sheet_p)
    print(f"Updated proof contact sheet: {sheet_p}")

    # Generate 7-frame head comparison strip
    frames_7 = [
        ("baseline", Image.open(PARTY_IDLE).convert("RGBA")),
        ("idle", Image.open(os.path.join(POSES_DIR, "idle.png")).convert("RGBA")),
        ("telegraph", Image.open(os.path.join(POSES_DIR, "telegraph.png")).convert("RGBA")),
        ("attack", Image.open(os.path.join(POSES_DIR, "attack.png")).convert("RGBA")),
        ("recover", Image.open(os.path.join(POSES_DIR, "recover.png")).convert("RGBA")),
        ("skill", Image.open(os.path.join(POSES_DIR, "skill.png")).convert("RGBA")),
        ("hit", Image.open(os.path.join(POSES_DIR, "hit.png")).convert("RGBA")),
    ]
    crops = []
    for _, im in frames_7:
        c = im.crop((35, 12, 95, 60))
        c_4x = c.resize((60 * 4, 48 * 4), Image.Resampling.NEAREST)
        crops.append(c_4x)
    strip_w = len(crops) * (60 * 4 + 4)
    strip_7 = Image.new("RGBA", (strip_w, 48 * 4), (210, 210, 210, 255))
    for idx, c in enumerate(crops):
        strip_7.paste(c, (idx * (60 * 4 + 4), 0), c)
    strip_p = os.path.join(PLAYER_DIR, "proof_lion_head_unification_7x.png")
    strip_7.save(strip_p)
    print(f"Generated 7-frame proof: {strip_p}")

if __name__ == "__main__":
    main()
