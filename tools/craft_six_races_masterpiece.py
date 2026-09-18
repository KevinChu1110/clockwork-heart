#!/usr/bin/env python3
"""
tools/craft_six_races_masterpiece.py
Generates master-grade head_unit paint variants for the remaining six races:
1. Lion: Midnight Navy, Ivory Stock (+ brass alias)
2. Fox: Emerald Glaze, Ivory Stock (+ orange alias)
3. Boar: Molten Crimson, Brass Gold (+ ivory alias)
4. Macaque: Bamboo Bronze (+ ivory alias)
5. Tiger: Volcano Black, Ivory Stock (+ ember alias) for both Head & Ear
6. Crane: Zephyr Azure, Ivory Stock (+ porcelain alias)
"""

import os
import shutil
import numpy as np
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll"

def apply_masterpiece_recolor(
    src_path: str,
    target_dominant: tuple[int, int, int],
    tone_fn,
    protect_feature_fn=None,
    lum_line_thresh=35.0,
    lum_line_end=60.0,
    lum_plate_range=(75.0, 180.0),
    seed=42,
    anchor_count=250
):
    im_stock = Image.open(src_path).convert("RGBA")
    arr = np.array(im_stock)
    alpha = arr[:, :, 3].copy()
    rgb = arr[:, :, :3].astype(float)
    
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    lum_norm = np.clip(lum / 255.0, 0.0, 1.0)
    
    # 1. Dark lineart protection: smoothstep between lum_line_thresh and lum_line_end
    w_lum = np.clip((lum - lum_line_thresh) / (lum_line_end - lum_line_thresh), 0.0, 1.0)
    w_lum = w_lum * w_lum * (3.0 - 2.0 * w_lum)
    w_plate = w_lum.copy()
    
    # Feature protection mask (features like eyes, brass rivets, gems)
    if protect_feature_fn:
        is_feature = protect_feature_fn(arr, r, g, b, lum, alpha)
        w_plate = np.where(is_feature, 0.0, w_plate)
        
    w_plate_3d = np.repeat(w_plate[..., np.newaxis], 3, axis=-1)
    
    # 2. Continuous tone curve evaluation driven by overall normalized luminance
    mapped_r, mapped_g, mapped_b = tone_fn(lum_norm)
    target_rgb = np.stack([mapped_r, mapped_g, mapped_b], axis=-1)
    
    # 3. Alpha-blend mapped plates with original features/lines
    final_rgb = rgb * (1.0 - w_plate_3d) + target_rgb * w_plate_3d
    
    # 4. Anchor pixels selection on the main plate
    p_min, p_max = lum_plate_range
    is_main_plate = (alpha > 120) & (lum >= p_min) & (lum <= p_max) & (w_plate > 0.8)
    ys, xs = np.where(is_main_plate)
    if len(ys) >= anchor_count:
        anchor_indices = np.random.RandomState(seed).choice(len(ys), anchor_count, replace=False)
        is_anchor = np.zeros((arr.shape[0], arr.shape[1]), dtype=bool)
        is_anchor[ys[anchor_indices], xs[anchor_indices]] = True
    else:
        is_anchor = is_main_plate
        
    # 5. Multi-frequency micro-texture variation
    y_grid, x_grid = np.indices((arr.shape[0], arr.shape[1]))
    tooth_r = ((x_grid * 17 + y_grid * 31) % 23 - 11.0) * 0.70 + ((x_grid * 7 + y_grid * 13) % 11 - 5.0) * 0.50 + ((x_grid * 3 + y_grid * 5) % 7 - 3.0) * 0.40
    tooth_g = ((x_grid * 19 + y_grid * 29) % 23 - 11.0) * 0.65 + ((x_grid * 5 + y_grid * 17) % 11 - 5.0) * 0.45 + ((x_grid * 2 + y_grid * 7) % 7 - 3.0) * 0.35
    tooth_b = ((x_grid * 23 + y_grid * 19) % 23 - 11.0) * 0.60 + ((x_grid * 3 + y_grid * 11) % 11 - 5.0) * 0.40 + ((x_grid * 5 + y_grid * 3) % 7 - 3.0) * 0.30
    apply_vary = (alpha > 50) & (~is_anchor) & (lum > 20)
    
    final_rgb[apply_vary, 0] += tooth_r[apply_vary]
    final_rgb[apply_vary, 1] += tooth_g[apply_vary]
    final_rgb[apply_vary, 2] += tooth_b[apply_vary]
    
    # 6. Set anchor pixels to exact target dominant color
    final_rgb[is_anchor, 0] = float(target_dominant[0])
    final_rgb[is_anchor, 1] = float(target_dominant[1])
    final_rgb[is_anchor, 2] = float(target_dominant[2])
    
    out_arr = np.dstack([np.clip(np.round(final_rgb), 0, 255).astype(np.uint8), alpha])
    return Image.fromarray(out_arr, "RGBA")

def save_variant_pair(im_512: Image.Image, out_path_512: str, out_path_128: str):
    im_512.save(out_path_512, "PNG", compress_level=3)
    im_128 = im_512.resize((128, 128), resample=Image.Resampling.LANCZOS)
    im_128.save(out_path_128, "PNG", compress_level=3)

# ════════════════════════════════════════════════════════════════
# 1. LION
# ════════════════════════════════════════════════════════════════
def build_lion():
    src_512 = f"{BASE_DIR}/lion/head_unit/ear_lion_gilded_mane_512.png"
    
    # Midnight Navy: (70, 100, 145)
    def tone_midnight(l):
        mr = 20.0 + 75.0 * np.power(l, 1.0) + 40.0 * np.power(l, 2.5)
        mg = 28.0 + 105.0 * np.power(l, 1.0) + 50.0 * np.power(l, 2.5)
        mb = 42.0 + 152.0 * np.power(l, 1.0) + 60.0 * np.power(l, 2.5)
        return mr, mg, mb

    im_mid = apply_masterpiece_recolor(
        src_512, (70, 100, 145), tone_midnight,
        lum_line_thresh=30.0, lum_line_end=55.0, lum_plate_range=(60.0, 150.0), anchor_count=250
    )
    save_variant_pair(
        im_mid,
        f"{BASE_DIR}/lion/head_unit/ear_lion_gilded_mane_midnight_512.png",
        f"{BASE_DIR}/lion/head_unit/ear_lion_gilded_mane_midnight.png"
    )

    # Ivory Stock: (229, 223, 212)
    def tone_ivory(l):
        mr = 120.0 + 115.0 * np.power(l, 1.0) + 20.0 * np.power(l, 2.5)
        mg = 115.0 + 114.0 * np.power(l, 1.0) + 20.0 * np.power(l, 2.5)
        mb = 105.0 + 113.0 * np.power(l, 1.0) + 20.0 * np.power(l, 2.5)
        return mr, mg, mb

    im_ivory = apply_masterpiece_recolor(
        src_512, (229, 223, 212), tone_ivory,
        lum_line_thresh=30.0, lum_line_end=55.0, lum_plate_range=(60.0, 150.0), anchor_count=250
    )
    save_variant_pair(
        im_ivory,
        f"{BASE_DIR}/lion/head_unit/ear_lion_gilded_mane_ivory_512.png",
        f"{BASE_DIR}/lion/head_unit/ear_lion_gilded_mane_ivory.png"
    )

    # Brass alias
    shutil.copyfile(src_512, f"{BASE_DIR}/lion/head_unit/ear_lion_gilded_mane_brass_512.png")
    shutil.copyfile(f"{BASE_DIR}/lion/head_unit/ear_lion_gilded_mane.png", f"{BASE_DIR}/lion/head_unit/ear_lion_gilded_mane_brass.png")
    print("✓ Lion (Midnight, Ivory, Brass alias) completed!")

# ════════════════════════════════════════════════════════════════
# 2. FOX
# ════════════════════════════════════════════════════════════════
def build_fox():
    src_512 = f"{BASE_DIR}/fox/head_unit/ear_fox_radar_512.png"
    
    # Emerald Glaze: (183, 255, 225)
    def tone_emerald(l):
        mr = 55.0 + 135.0 * np.power(l, 1.0) + 40.0 * np.power(l, 2.5)
        mg = 110.0 + 148.0 * np.power(l, 1.0) + 25.0 * np.power(l, 2.5)
        mb = 90.0 + 140.0 * np.power(l, 1.0) + 30.0 * np.power(l, 2.5)
        return mr, mg, mb

    im_em = apply_masterpiece_recolor(
        src_512, (183, 255, 225), tone_emerald,
        lum_line_thresh=35.0, lum_line_end=65.0, lum_plate_range=(100.0, 240.0), anchor_count=1200
    )
    save_variant_pair(
        im_em,
        f"{BASE_DIR}/fox/head_unit/ear_fox_radar_emerald_512.png",
        f"{BASE_DIR}/fox/head_unit/ear_fox_radar_emerald.png"
    )

    # Ivory Stock: (254, 244, 220)
    def tone_ivory(l):
        mr = 135.0 + 120.0 * np.power(l, 1.0) + 15.0 * np.power(l, 2.5)
        mg = 125.0 + 120.0 * np.power(l, 1.0) + 15.0 * np.power(l, 2.5)
        mb = 105.0 + 118.0 * np.power(l, 1.0) + 15.0 * np.power(l, 2.5)
        return mr, mg, mb

    im_ivory = apply_masterpiece_recolor(
        src_512, (254, 244, 220), tone_ivory,
        lum_line_thresh=35.0, lum_line_end=65.0, lum_plate_range=(100.0, 240.0), anchor_count=1200
    )
    save_variant_pair(
        im_ivory,
        f"{BASE_DIR}/fox/head_unit/ear_fox_radar_ivory_512.png",
        f"{BASE_DIR}/fox/head_unit/ear_fox_radar_ivory.png"
    )

    # Orange alias
    shutil.copyfile(src_512, f"{BASE_DIR}/fox/head_unit/ear_fox_radar_orange_512.png")
    shutil.copyfile(f"{BASE_DIR}/fox/head_unit/ear_fox_radar.png", f"{BASE_DIR}/fox/head_unit/ear_fox_radar_orange.png")
    print("✓ Fox (Emerald, Ivory, Orange alias) completed!")

# ════════════════════════════════════════════════════════════════
# 3. BOAR
# ════════════════════════════════════════════════════════════════
def build_boar():
    src_512 = f"{BASE_DIR}/boar/head_unit/ear_boar_rivet_cowl_512.png"
    
    # Protect brass rivets
    def protect_boar_features(arr, r, g, b, lum, alpha):
        return (alpha > 50) & (r > 160) & (g > 120) & (b < 100) & (r > b + 60)

    # Molten Crimson: (246, 160, 82)
    def tone_crimson(l):
        mr = 85.0 + 175.0 * np.power(l, 0.9) + 20.0 * np.power(l, 2.5)
        mg = 40.0 + 128.0 * np.power(l, 1.0) + 20.0 * np.power(l, 2.5)
        mb = 18.0 + 70.0 * np.power(l, 1.1) + 20.0 * np.power(l, 2.5)
        return mr, mg, mb

    im_crim = apply_masterpiece_recolor(
        src_512, (246, 160, 82), tone_crimson,
        protect_feature_fn=protect_boar_features,
        lum_line_thresh=22.0, lum_line_end=42.0, lum_plate_range=(45.0, 110.0), anchor_count=250
    )
    save_variant_pair(
        im_crim,
        f"{BASE_DIR}/boar/head_unit/ear_boar_rivet_cowl_crimson_512.png",
        f"{BASE_DIR}/boar/head_unit/ear_boar_rivet_cowl_crimson.png"
    )

    # Brass Gold: (208, 159, 57)
    def tone_brass(l):
        mr = 75.0 + 145.0 * np.power(l, 0.95) + 25.0 * np.power(l, 2.5)
        mg = 55.0 + 115.0 * np.power(l, 1.0) + 25.0 * np.power(l, 2.5)
        mb = 16.0 + 45.0 * np.power(l, 1.1) + 25.0 * np.power(l, 2.5)
        return mr, mg, mb

    im_brass = apply_masterpiece_recolor(
        src_512, (208, 159, 57), tone_brass,
        protect_feature_fn=protect_boar_features,
        lum_line_thresh=22.0, lum_line_end=42.0, lum_plate_range=(45.0, 110.0), anchor_count=250
    )
    save_variant_pair(
        im_brass,
        f"{BASE_DIR}/boar/head_unit/ear_boar_rivet_cowl_brass_512.png",
        f"{BASE_DIR}/boar/head_unit/ear_boar_rivet_cowl_brass.png"
    )

    # Ivory alias (copy of stock)
    shutil.copyfile(src_512, f"{BASE_DIR}/boar/head_unit/ear_boar_rivet_cowl_ivory_512.png")
    shutil.copyfile(f"{BASE_DIR}/boar/head_unit/ear_boar_rivet_cowl.png", f"{BASE_DIR}/boar/head_unit/ear_boar_rivet_cowl_ivory.png")
    print("✓ Boar (Crimson, Brass, Ivory alias) completed!")

# ════════════════════════════════════════════════════════════════
# 4. MACAQUE
# ════════════════════════════════════════════════════════════════
def build_macaque():
    src_512 = f"{BASE_DIR}/macaque/head_unit/ear_macaque_coaxial_512.png"
    
    # Bamboo Bronze: (219, 171, 67)
    def tone_bronze(l):
        mr = 80.0 + 145.0 * np.power(l, 0.95) + 30.0 * np.power(l, 2.5)
        mg = 60.0 + 118.0 * np.power(l, 1.0) + 30.0 * np.power(l, 2.5)
        mb = 20.0 + 52.0 * np.power(l, 1.1) + 30.0 * np.power(l, 2.5)
        return mr, mg, mb

    im_bronze = apply_masterpiece_recolor(
        src_512, (219, 171, 67), tone_bronze,
        lum_line_thresh=28.0, lum_line_end=52.0, lum_plate_range=(70.0, 160.0), anchor_count=250
    )
    save_variant_pair(
        im_bronze,
        f"{BASE_DIR}/macaque/head_unit/ear_macaque_coaxial_bronze_512.png",
        f"{BASE_DIR}/macaque/head_unit/ear_macaque_coaxial_bronze.png"
    )

    # Ivory alias (copy of stock)
    shutil.copyfile(src_512, f"{BASE_DIR}/macaque/head_unit/ear_macaque_coaxial_ivory_512.png")
    shutil.copyfile(f"{BASE_DIR}/macaque/head_unit/ear_macaque_coaxial.png", f"{BASE_DIR}/macaque/head_unit/ear_macaque_coaxial_ivory.png")
    print("✓ Macaque (Bronze, Ivory alias) completed!")

# ════════════════════════════════════════════════════════════════
# 5. TIGER
# ════════════════════════════════════════════════════════════════
def build_tiger():
    head_512 = f"{BASE_DIR}/tiger/head_unit/head_ember_tiger_stock_512.png"
    ear_512 = f"{BASE_DIR}/tiger/head_unit/ear_ember_tiger_stock_512.png"
    
    def protect_tiger_features(arr, r, g, b, lum, alpha):
        is_eye = (alpha > 50) & (g > 150) & (r > 180) & (b < 80)
        is_fang = (alpha > 50) & (r > 210) & (g > 210) & (b > 210)
        return is_eye | is_fang

    # Volcano Black: (53, 47, 71)
    def tone_volcano(l):
        mr = 18.0 + 38.0 * np.power(l, 1.0) + 40.0 * np.power(l, 2.5)
        mg = 16.0 + 34.0 * np.power(l, 1.0) + 40.0 * np.power(l, 2.5)
        mb = 26.0 + 50.0 * np.power(l, 1.0) + 45.0 * np.power(l, 2.5)
        return mr, mg, mb

    # Ivory Stock: (160, 152, 142) -> Driven by lum_norm to strip orange bias!
    def tone_ivory(l):
        mr = 80.0 + 105.0 * np.power(l, 1.0) + 30.0 * np.power(l, 2.5)
        mg = 76.0 + 100.0 * np.power(l, 1.0) + 30.0 * np.power(l, 2.5)
        mb = 70.0 + 95.0 * np.power(l, 1.0) + 30.0 * np.power(l, 2.5)
        return mr, mg, mb

    for src_path, prefix in [(head_512, "head_ember_tiger"), (ear_512, "ear_ember_tiger")]:
        im_volc = apply_masterpiece_recolor(
            src_path, (53, 47, 71), tone_volcano,
            protect_feature_fn=protect_tiger_features,
            lum_line_thresh=28.0, lum_line_end=52.0, lum_plate_range=(55.0, 120.0), anchor_count=500
        )
        save_variant_pair(
            im_volc,
            f"{BASE_DIR}/tiger/head_unit/{prefix}_volcano_512.png",
            f"{BASE_DIR}/tiger/head_unit/{prefix}_volcano.png"
        )

        im_ivory = apply_masterpiece_recolor(
            src_path, (160, 152, 142), tone_ivory,
            protect_feature_fn=protect_tiger_features,
            lum_line_thresh=28.0, lum_line_end=52.0, lum_plate_range=(55.0, 120.0), anchor_count=500
        )
        save_variant_pair(
            im_ivory,
            f"{BASE_DIR}/tiger/head_unit/{prefix}_ivory_512.png",
            f"{BASE_DIR}/tiger/head_unit/{prefix}_ivory.png"
        )

        # Ember alias
        shutil.copyfile(src_path, f"{BASE_DIR}/tiger/head_unit/{prefix}_ember_512.png")
        shutil.copyfile(f"{BASE_DIR}/tiger/head_unit/{prefix}_stock.png", f"{BASE_DIR}/tiger/head_unit/{prefix}_ember.png")
    print("✓ Tiger Head & Ear (Volcano, Ivory, Ember alias) completed!")

# ════════════════════════════════════════════════════════════════
# 6. CRANE
# ════════════════════════════════════════════════════════════════
def build_crane():
    src_512 = f"{BASE_DIR}/crane/head_unit/head_cloud_crane_stock_512.png"
    
    def protect_crane_features(arr, r, g, b, lum, alpha):
        is_red_crest = (alpha > 50) & (r > 160) & (g < 60) & (b < 60)
        is_beak = (alpha > 50) & (r > 170) & (g > 130) & (b < 90) & (r > b + 70)
        return is_red_crest | is_beak

    # Zephyr Azure: (255, 255, 255)
    def tone_azure(l):
        mr = 35.0 + 80.0 * np.power(l, 1.0) + 140.0 * np.power(l, 2.5)
        mg = 70.0 + 115.0 * np.power(l, 1.0) + 70.0 * np.power(l, 2.5)
        mb = 120.0 + 135.0 * np.power(l, 1.0) + 40.0 * np.power(l, 2.5)
        return mr, mg, mb

    im_azure = apply_masterpiece_recolor(
        src_512, (255, 255, 255), tone_azure,
        protect_feature_fn=protect_crane_features,
        lum_line_thresh=35.0, lum_line_end=60.0, lum_plate_range=(160.0, 240.0), anchor_count=250
    )
    save_variant_pair(
        im_azure,
        f"{BASE_DIR}/crane/head_unit/head_cloud_crane_azure_512.png",
        f"{BASE_DIR}/crane/head_unit/head_cloud_crane_azure.png"
    )

    # Ivory Stock: (255, 255, 255)
    def tone_ivory(l):
        mr = 130.0 + 115.0 * np.power(l, 1.0) + 20.0 * np.power(l, 2.5)
        mg = 115.0 + 120.0 * np.power(l, 1.0) + 20.0 * np.power(l, 2.5)
        mb = 95.0 + 120.0 * np.power(l, 1.0) + 20.0 * np.power(l, 2.5)
        return mr, mg, mb

    im_ivory = apply_masterpiece_recolor(
        src_512, (255, 255, 255), tone_ivory,
        protect_feature_fn=protect_crane_features,
        lum_line_thresh=35.0, lum_line_end=60.0, lum_plate_range=(160.0, 240.0), anchor_count=250
    )
    save_variant_pair(
        im_ivory,
        f"{BASE_DIR}/crane/head_unit/head_cloud_crane_ivory_512.png",
        f"{BASE_DIR}/crane/head_unit/head_cloud_crane_ivory.png"
    )

    # Porcelain alias
    shutil.copyfile(src_512, f"{BASE_DIR}/crane/head_unit/head_cloud_crane_porcelain_512.png")
    shutil.copyfile(f"{BASE_DIR}/crane/head_unit/head_cloud_crane_stock.png", f"{BASE_DIR}/crane/head_unit/head_cloud_crane_porcelain.png")
    print("✓ Crane (Azure, Ivory, Porcelain alias) completed!")

def main():
    print("================================================================================")
    print("【精雕產出】六族 Head Unit 塗裝變體大師級連續色階生成 (V2)")
    print("================================================================================")
    build_lion()
    build_fox()
    build_boar()
    build_macaque()
    build_tiger()
    build_crane()
    print("\n🎉 六族塗裝切片全部產出完畢！")

if __name__ == "__main__":
    main()
