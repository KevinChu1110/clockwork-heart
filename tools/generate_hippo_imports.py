#!/usr/bin/env python3
import hashlib
import os
import random
import string

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

def make_uid():
    chars = string.ascii_lowercase + string.digits
    return "uid://" + "".join(random.choices(chars, k=13))

game_dir = os.path.join(REPO_ROOT, "game")
generated_count = 0
for root, dirs, files in os.walk(game_dir):
    for f in files:
        if ("hippo" in f or "poses/hippo" in root) and f.endswith(".png"):
            full_path = os.path.join(root, f)
            import_path = full_path + ".import"
            if not os.path.exists(import_path):
                res_path = "res://" + os.path.relpath(full_path, game_dir).replace("\\", "/")
                md5 = hashlib.md5(res_path.encode("utf-8")).hexdigest()
                base_name = f
                uid = make_uid()
                content = template.format(uid=uid, base_name=base_name, md5=md5, res_path=res_path)
                with open(import_path, "w", encoding="utf-8") as out_f:
                    out_f.write(content)
                generated_count += 1
                print(f"✓ Generated {os.path.relpath(import_path, REPO_ROOT)}")

print(f"Total .import files generated: {generated_count}")
