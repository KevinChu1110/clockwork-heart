#!/usr/bin/env python3
import hashlib
import os
import random
import string

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

files = [
    "game/assets/sprites/player/poses/crab/idle.png",
    "game/assets/sprites/player/poses/crab/idle_512.png",
    "game/assets/sprites/player/poses/crab/telegraph.png",
    "game/assets/sprites/player/poses/crab/telegraph_512.png",
    "game/assets/sprites/player/poses/crab/attack.png",
    "game/assets/sprites/player/poses/crab/attack_512.png",
    "game/assets/sprites/player/poses/crab/skill.png",
    "game/assets/sprites/player/poses/crab/skill_512.png",
    "game/assets/sprites/player/poses/crab/hit.png",
    "game/assets/sprites/player/poses/crab/hit_512.png",
    "game/assets/sprites/player/poses/crab/recover.png",
    "game/assets/sprites/player/poses/crab/recover_512.png",
    "game/assets/sprites/player/proof_crab_combat_poses_768.png",
    "game/assets/sprites/player/proof_crab_combat_poses_magenta.png",
]

def make_uid():
    chars = string.ascii_lowercase + string.digits
    return "uid://" + "".join(random.choices(chars, k=13))

template = """[remap]

importer="texture"
type="CompressedTexture2D"
uid="{uid}"
path="res://.godot/imported/{base_name}-{md5}.ctex"
metadata={{
"vram_texture": false
}}

[deps]

source_file="{res_path}"
dest_files=["res://.godot/imported/{base_name}-{md5}.ctex"]

[params]

compress/mode=0
compress/high_quality=false
compress/lossy_quality=0.7
compress/uastc_level=0
compress/rdo_quality_loss=0.0
compress/hdr_compression=1
compress/normal_map=0
compress/channel_pack=0
mipmaps/generate=false
mipmaps/limit=-1
roughness/mode=0
roughness/src_normal=""
process/channel_remap/red=0
process/channel_remap/green=1
process/channel_remap/blue=2
process/channel_remap/alpha=3
process/fix_alpha_border=true
process/premult_alpha=false
process/normal_map_invert_y=false
process/hdr_as_srgb=false
process/hdr_clamp_exposure=false
process/size_limit=0
detect_3d/compress_to=1
"""

for rel_f in files:
    full_path = os.path.join(REPO_ROOT, rel_f)
    if not os.path.exists(full_path):
        print(f"Skipping {full_path} (does not exist)")
        continue
    # res_path relative to game/
    res_path = "res://" + os.path.relpath(full_path, os.path.join(REPO_ROOT, "game"))
    md5 = hashlib.md5(res_path.encode("utf-8")).hexdigest()
    base_name = os.path.basename(full_path)
    uid = make_uid()
    content = template.format(uid=uid, base_name=base_name, md5=md5, res_path=res_path)
    import_path = full_path + ".import"
    with open(import_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Generated {os.path.basename(import_path)}")
