#!/usr/bin/env python3
import hashlib
import os
import random
import string

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

files = [
    "game/assets/sprites/player/walrus_battle.png",
    "game/assets/sprites/player/walrus_battle_512.png",
    "game/assets/sprites/player/proof_walrus_idle_vs_battle.png",
    "game/assets/sprites/player/proof_walrus_idle_vs_battle_512.png",
    "game/assets/sprites/player/walrus_walk_0.png",
    "game/assets/sprites/player/walrus_walk_1.png",
    "game/assets/sprites/player/walrus_walk_2.png",
    "game/assets/sprites/player/walrus_walk_3.png",
    "game/assets/sprites/player/walrus_walk_0_x3.png",
    "game/assets/sprites/player/walrus_walk_1_x3.png",
    "game/assets/sprites/player/walrus_walk_2_x3.png",
    "game/assets/sprites/player/walrus_walk_3_x3.png",
    "game/assets/sprites/player/walrus_walk_0_512.png",
    "game/assets/sprites/player/walrus_walk_1_512.png",
    "game/assets/sprites/player/walrus_walk_2_512.png",
    "game/assets/sprites/player/walrus_walk_3_512.png",
    "game/assets/sprites/player/proof_walrus_walk_cycle.png",
    "game/assets/sprites/portraits/walrus.png",
    "game/assets/sprites/portraits/walrus_512.png",
    "game/assets/sprites/portraits/icebreaker_walrus.png",
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
    import_path = full_path + ".import"
    if os.path.exists(import_path):
        print(f"Existing {os.path.basename(import_path)} kept")
        continue
    res_path = "res://" + os.path.relpath(full_path, os.path.join(REPO_ROOT, "game"))
    md5 = hashlib.md5(res_path.encode("utf-8")).hexdigest()
    base_name = os.path.basename(full_path)
    uid = make_uid()
    content = template.format(uid=uid, base_name=base_name, md5=md5, res_path=res_path)
    with open(import_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Generated {os.path.basename(import_path)}")
