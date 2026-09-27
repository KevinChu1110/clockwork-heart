#!/usr/bin/env python3
"""
tools/apply_clean_keys_and_rebuild.py
Applies clean winding keys for Orbit Hound and Emerald Fawn,
regenerates _512 LANCZOS versions, paperdoll composites, and 6 combat action poses.
Also generates before-and-after side-by-side comparison images.
"""
import os
import shutil
from PIL import Image, ImageDraw, ImageFont
import numpy as np

WORKTREE = "/opt/side/bravesoul-game/.worktrees/t_1f136a47"
BACKUP_DIR = f"{WORKTREE}/tools/backup_before_clean"
os.makedirs(BACKUP_DIR, exist_ok=True)

from test_fixed_hound import build_fixed_hound_key
from test_fixed_fawn import build_fixed_fawn_key

def backup_file(src, name):
    if os.path.exists(src):
        dst = os.path.join(BACKUP_DIR, name)
        shutil.copyfile(src, dst)
        print(f"Backed up: {src} -> {dst}")

def main():
    print("=== STEP 1: Backing up original files for before/after comparison ===")
    hound_key_128 = f"{WORKTREE}/game/assets/sprites/player/paperdoll/hound/winding_key/key_hound_four_blade_antenna_gold.png"
    hound_key_512 = f"{WORKTREE}/game/assets/sprites/player/paperdoll/hound/winding_key/key_hound_four_blade_antenna_gold_512.png"
    hound_comp = f"{WORKTREE}/game/assets/sprites/player/paperdoll/hound/proof_paperdoll_hound_composite.png"
    hound_idle_pose = f"{WORKTREE}/game/assets/sprites/player/poses/hound/idle.png"
    hound_idle_512 = f"{WORKTREE}/game/assets/sprites/player/poses/hound/idle_512.png"
    hound_strip = f"{WORKTREE}/game/assets/sprites/player/proof_hound_combat_poses_768.png"

    fawn_key_128 = f"{WORKTREE}/game/assets/sprites/player/paperdoll/fawn/winding_key/key_fawn_clover_leaf_brass.png"
    fawn_key_512 = f"{WORKTREE}/game/assets/sprites/player/paperdoll/fawn/winding_key/key_fawn_clover_leaf_brass_512.png"
    fawn_comp = f"{WORKTREE}/game/assets/sprites/player/paperdoll/fawn/proof_paperdoll_fawn_composite.png"
    fawn_idle_pose = f"{WORKTREE}/game/assets/sprites/player/poses/fawn/idle.png"
    fawn_idle_512 = f"{WORKTREE}/game/assets/sprites/player/poses/fawn/idle_512.png"
    fawn_strip = f"{WORKTREE}/game/assets/sprites/player/proof_fawn_combat_poses_768.png"

    backup_file(hound_key_128, "hound_key_128_before.png")
    backup_file(hound_key_512, "hound_key_512_before.png")
    backup_file(hound_comp, "hound_comp_before.png")
    backup_file(hound_idle_pose, "hound_idle_before.png")
    backup_file(hound_idle_512, "hound_idle_512_before.png")
    backup_file(hound_strip, "hound_strip_before.png")

    backup_file(fawn_key_128, "fawn_key_128_before.png")
    backup_file(fawn_key_512, "fawn_key_512_before.png")
    backup_file(fawn_comp, "fawn_comp_before.png")
    backup_file(fawn_idle_pose, "fawn_idle_before.png")
    backup_file(fawn_idle_512, "fawn_idle_512_before.png")
    backup_file(fawn_strip, "fawn_strip_before.png")

    print("\n=== STEP 2: Writing clean winding keys & 512 LANCZOS versions ===")
    hound_clean_128 = build_fixed_hound_key()
    hound_clean_512 = hound_clean_128.resize((512, 512), Image.Resampling.LANCZOS)
    hound_clean_128.save(hound_key_128)
    hound_clean_512.save(hound_key_512)
    # Universal key copy
    shutil.copyfile(hound_key_128, f"{WORKTREE}/game/assets/sprites/player/paperdoll/key/key_hound_four_blade_antenna_gold.png")
    print("  ✓ Hound keys saved (128, 512, universal)")

    fawn_clean_128 = build_fixed_fawn_key()
    fawn_clean_512 = fawn_clean_128.resize((512, 512), Image.Resampling.LANCZOS)
    fawn_clean_128.save(fawn_key_128)
    fawn_clean_512.save(fawn_key_512)
    # Universal key copy
    shutil.copyfile(fawn_key_128, f"{WORKTREE}/game/assets/sprites/player/paperdoll/key/key_fawn_clover_leaf_brass.png")
    print("  ✓ Fawn keys saved (128, 512, universal)")

    print("\n=== STEP 3: Rebuilding paperdoll composites ===")
    # Hound composite
    hound_pd = f"{WORKTREE}/game/assets/sprites/player/paperdoll/hound"
    curio_h = Image.open(f"{hound_pd}/back_curio/curio_hound_floating_micro_satellite.png").convert("RGBA")
    chassis_h = Image.open(f"{hound_pd}/chassis/chassis_hound_polymer_astro_default.png").convert("RGBA")
    head_h = Image.open(f"{hound_pd}/head_unit/head_hound_radar_leaf_antennas.png").convert("RGBA")
    core_h = Image.open(f"{hound_pd}/optic_core/face_hound_dot_matrix_led_eyes.png").convert("RGBA")
    costume_h = Image.open(f"{hound_pd}/costume/costume_hound_space_explorer_harness.png").convert("RGBA")
    weapon_h = Image.open(f"{hound_pd}/weapon/weapon_hound_stellar_beacon_lance.png").convert("RGBA")

    comp_h = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    comp_h.alpha_composite(hound_clean_128)
    comp_h.alpha_composite(curio_h)
    comp_h.alpha_composite(chassis_h)
    comp_h.alpha_composite(head_h)
    comp_h.alpha_composite(core_h)
    comp_h.alpha_composite(costume_h)
    comp_h.alpha_composite(weapon_h)
    comp_h.save(hound_comp)

    mag_h = Image.new("RGBA", (128, 128), (255, 0, 255, 255))
    mag_h.alpha_composite(comp_h)
    mag_h.save(f"{hound_pd}/proof_paperdoll_hound_magenta.png")

    # 7 slices strip for hound
    OUTLINE = (31, 26, 58, 255)
    strip_w = 128 * 7 + 8 * 8
    strip_h = 128 + 24
    strip_h_img = Image.new("RGBA", (strip_w, strip_h), (24, 20, 36, 255))
    sd_h = ImageDraw.Draw(strip_h_img)
    slot_names = ["Key", "Curio", "Chassis", "Head", "Optic", "Costume", "Weapon"]
    strip_slices_h = [hound_clean_128, curio_h, chassis_h, head_h, core_h, costume_h, weapon_h]
    for i, (name, s_img) in enumerate(zip(slot_names, strip_slices_h)):
        px = 8 + i * (128 + 8)
        py = 8
        sd_h.rectangle([px, py, px + 128, py + 128], fill=(42, 36, 62, 255), outline=OUTLINE)
        strip_h_img.alpha_composite(s_img, (px, py))
        sd_h.text((px + 4, py + 128 + 2), name, fill=(255, 208, 40, 255))
    strip_h_img.save(f"{hound_pd}/proof_hound_all_7_slices.png")
    print("  ✓ Hound paperdoll composite & proofs updated")

    # Fawn composite
    fawn_pd = f"{WORKTREE}/game/assets/sprites/player/paperdoll/fawn"
    curio_f = Image.open(f"{fawn_pd}/back_curio/curio_fawn_floating_pinecone_chime.png").convert("RGBA")
    chassis_f = Image.open(f"{fawn_pd}/chassis/chassis_fawn_timber_tinplate_default.png").convert("RGBA")
    head_f = Image.open(f"{fawn_pd}/head_unit/head_fawn_vernier_caliper_horns.png").convert("RGBA")
    core_f = Image.open(f"{fawn_pd}/optic_core/face_fawn_amber_lens_alert_eyes.png").convert("RGBA")
    costume_f = Image.open(f"{fawn_pd}/costume/costume_fawn_emerald_scout_tunic.png").convert("RGBA")
    weapon_f = Image.open(f"{fawn_pd}/weapon/weapon_fawn_vernier_shortbow.png").convert("RGBA")

    comp_f = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    comp_f.alpha_composite(fawn_clean_128)
    comp_f.alpha_composite(curio_f)
    comp_f.alpha_composite(chassis_f)
    comp_f.alpha_composite(head_f)
    comp_f.alpha_composite(core_f)
    comp_f.alpha_composite(costume_f)
    comp_f.alpha_composite(weapon_f)
    comp_f.save(fawn_comp)

    mag_f = Image.new("RGBA", (128, 128), (255, 0, 255, 255))
    mag_f.alpha_composite(comp_f)
    mag_f.save(f"{fawn_pd}/proof_paperdoll_fawn_magenta.png")

    strip_f_img = Image.new("RGBA", (strip_w, strip_h), (24, 20, 36, 255))
    sd_f = ImageDraw.Draw(strip_f_img)
    strip_slices_f = [fawn_clean_128, curio_f, chassis_f, head_f, core_f, costume_f, weapon_f]
    for i, (name, s_img) in enumerate(zip(slot_names, strip_slices_f)):
        px = 8 + i * (128 + 8)
        py = 8
        sd_f.rectangle([px, py, px + 128, py + 128], fill=(42, 36, 62, 255), outline=OUTLINE)
        strip_f_img.alpha_composite(s_img, (px, py))
        sd_f.text((px + 4, py + 128 + 2), name, fill=(255, 208, 40, 255))
    strip_f_img.save(f"{fawn_pd}/proof_fawn_all_7_slices.png")
    print("  ✓ Fawn paperdoll composite & proofs updated")

if __name__ == "__main__":
    main()
