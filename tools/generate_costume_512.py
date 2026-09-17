import os
from PIL import Image

TARGETS = [
    ("rabbit", "costume_royal_parade"),
    ("rabbit", "costume_steam_artisan"),
    ("fox", "costume_astral_observer"),
    ("boar", "costume_viking_ironclad"),
    ("macaque", "costume_zen_striker"),
    ("tiger", "costume_ash_ninja_garb"),
    ("tiger", "costume_ember_tunic"),
    ("crane", "costume_sky_hunter_mail"),
    ("crane", "costume_zephyr_robe"),
    ("bear", "costume_berserker_cuirass"),
    ("bear", "costume_ironclad_overalls"),
    ("penguin", "costume_navigator_harness"),
    ("penguin", "costume_abyssal_diver_cuirass"),
]

BASE_DIR = "game/assets/sprites/player/paperdoll"

created = []
for race, item in TARGETS:
    costume_dir = os.path.join(BASE_DIR, race, "costume")
    src_128 = os.path.join(costume_dir, f"{item}.png")
    dst_512 = os.path.join(costume_dir, f"{item}_512.png")
    
    assert os.path.exists(src_128), f"Source 128 not found: {src_128}"
    
    img = Image.open(src_128).convert("RGBA")
    assert img.size == (128, 128), f"Expected 128x128, got {img.size} for {src_128}"
    
    # Resize using LANCZOS
    img_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
    assert img_512.size == (512, 512), f"Expected 512x512, got {img_512.size}"
    
    img_512.save(dst_512, format="PNG")
    created.append(dst_512)
    print(f"Generated [LANCZOS]: {dst_512} (size: {img_512.size})")

print(f"\nSuccessfully generated all {len(created)} 512 costume textures.")
