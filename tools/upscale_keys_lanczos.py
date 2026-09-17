import os
from PIL import Image

keys_to_upscale = [
    ("game/assets/sprites/player/paperdoll/bear/winding_key/key_cross_pendulum.png",
     "game/assets/sprites/player/paperdoll/bear/winding_key/key_cross_pendulum_512.png"),
    ("game/assets/sprites/player/paperdoll/crane/winding_key/key_tri_wing_zephyr.png",
     "game/assets/sprites/player/paperdoll/crane/winding_key/key_tri_wing_zephyr_512.png"),
    ("game/assets/sprites/player/paperdoll/penguin/winding_key/key_twin_ring_helm.png",
     "game/assets/sprites/player/paperdoll/penguin/winding_key/key_twin_ring_helm_512.png"),
    ("game/assets/sprites/player/paperdoll/tiger/winding_key/key_turbine_flame.png",
     "game/assets/sprites/player/paperdoll/tiger/winding_key/key_turbine_flame_512.png"),
    ("game/assets/sprites/player/paperdoll/key/key_cross_pendulum.png",
     "game/assets/sprites/player/paperdoll/key/key_cross_pendulum_512.png"),
    ("game/assets/sprites/player/paperdoll/key/key_tri_wing_zephyr.png",
     "game/assets/sprites/player/paperdoll/key/key_tri_wing_zephyr_512.png"),
    ("game/assets/sprites/player/paperdoll/key/key_twin_ring_helm.png",
     "game/assets/sprites/player/paperdoll/key/key_twin_ring_helm_512.png"),
    ("game/assets/sprites/player/paperdoll/key/key_turbine_flame.png",
     "game/assets/sprites/player/paperdoll/key/key_turbine_flame_512.png"),
]

for src, dst in keys_to_upscale:
    if os.path.exists(src):
        with Image.open(src) as img:
            rgba = img.convert("RGBA")
            resized = rgba.resize((512, 512), resample=Image.Resampling.LANCZOS)
            resized.save(dst, format="PNG")
            print(f"Upscaled {src} ({rgba.size}) -> {dst} (512x512) via LANCZOS")
    else:
        print(f"Warning: {src} not found")
