#!/usr/bin/env python3
import json
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"
PARTS_DIR = f"{BOAR_DIR}/maple_parts"
JSON_PATH = f"{REPO_ROOT}/game/data/tables/maple_paperdoll_boar.json"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    spec = json.load(f)

anchors = spec["anchors"]
neck = anchors["neck"] # [250, 176]
navel = anchors["navel"] # [256, 340]
hand = anchors["hand"] # [180, 340]
back_key = anchors["back_key"] # [360, 140]
brow_rel = anchors["brow_relative_to_neck"] # [-15, -15]
brow = [neck[0] + brow_rel[0], neck[1] + brow_rel[1]] # [235, 161]
tail = anchors["tail"] # [350, 335]

def composite_loadout(body_id, head_id, eye_id, costume_id, weapon_id, key_id, tail_id, out_name):
    canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))

    # 1. key (z=5)
    if key_id != "none":
        k_im = Image.open(f"{PARTS_DIR}/winding_key/{key_id}.png").convert("RGBA")
        k_orig = spec["parts"]["winding_key"]["items"][key_id]["origin"]
        pos = (back_key[0] - k_orig[0], back_key[1] - k_orig[1])
        canvas.alpha_composite(k_im, pos)

    # 2. tail (z=8)
    if tail_id != "none":
        t_im = Image.open(f"{PARTS_DIR}/back_curio/{tail_id}.png").convert("RGBA")
        t_orig = spec["parts"]["back_curio"]["items"][tail_id]["origin"]
        pos = (tail[0] - t_orig[0], tail[1] - t_orig[1])
        canvas.alpha_composite(t_im, pos)

    # 3. body (z=10)
    if body_id != "none":
        b_im = Image.open(f"{PARTS_DIR}/body/{body_id}.png").convert("RGBA")
        canvas.alpha_composite(b_im, (0, 0))

    # 4. head_unit (z=20)
    if head_id != "none":
        h_im = Image.open(f"{PARTS_DIR}/head_unit/{head_id}.png").convert("RGBA")
        h_orig = spec["parts"]["head_unit"]["items"][head_id]["origin"]
        pos = (neck[0] - h_orig[0], neck[1] - h_orig[1])
        canvas.alpha_composite(h_im, pos)

    # 5. costume (z=25)
    if costume_id != "none":
        c_im = Image.open(f"{PARTS_DIR}/costume/{costume_id}.png").convert("RGBA")
        c_orig = spec["parts"]["costume"]["items"][costume_id]["origin"]
        pos = (navel[0] - c_orig[0], navel[1] - c_orig[1])
        canvas.alpha_composite(c_im, pos)

    # 6. eyes (z=30)
    if eye_id != "none":
        e_im = Image.open(f"{PARTS_DIR}/eyes/{eye_id}.png").convert("RGBA")
        e_orig = spec["parts"]["eyes"]["items"][eye_id]["origin"]
        pos = (brow[0] - e_orig[0], brow[1] - e_orig[1])
        canvas.alpha_composite(e_im, pos)

    # 7. weapon (z=40)
    if weapon_id != "none":
        w_im = Image.open(f"{PARTS_DIR}/weapon/{weapon_id}.png").convert("RGBA")
        w_orig = spec["parts"]["weapon"]["items"][weapon_id]["origin"]
        pos = (hand[0] - w_orig[0], hand[1] - w_orig[1])
        canvas.alpha_composite(w_im, pos)

    canvas.save(f"/tmp/{out_name}.png")
    print(f"Saved /tmp/{out_name}.png, bbox={canvas.getbbox()}")

# 1. 預設全配裝 (Ironclad, Brass, Cyan eye, Greathammer, Key, Tail)
composite_loadout("paint_brass_gold", "ear_boar_rivet_cowl_brass", "eyes_cyan_emerald", "costume_viking_ironclad", "wpn_anvil_greathammer", "key_classic_brass", "curio_spring_tail", "boar_proof_default_ironclad")

# 2. 束帶外裝變體 (Harness)
composite_loadout("paint_brass_gold", "ear_boar_rivet_cowl_brass", "eyes_cyan_emerald", "costume_viking_harness", "wpn_anvil_greathammer", "key_classic_brass", "curio_spring_tail", "boar_proof_harness")

# 3. 裸機素體 (costume=none, eye=none) 驗證無破圖、素體純淨金屬底盤
composite_loadout("paint_brass_gold", "ear_boar_rivet_cowl_brass", "none", "none", "none", "key_classic_brass", "curio_spring_tail", "boar_proof_bare_chassis")

# 4. 赤焰塗裝 + 眨眼 (Molten Crimson, Amber eye, Ironclad)
composite_loadout("paint_molten_crimson", "ear_boar_rivet_cowl_crimson", "eyes_amber_gold", "costume_viking_ironclad", "wpn_anvil_greathammer", "key_classic_brass", "curio_spring_tail", "boar_proof_molten_crimson")

# 5. 眨眼測試 (Blink)
composite_loadout("paint_brass_gold", "ear_boar_rivet_cowl_brass", "eyes_blink", "costume_viking_ironclad", "wpn_anvil_greathammer", "key_classic_brass", "curio_spring_tail", "boar_proof_blink")
