import os
from PIL import Image

races = ["fox", "lion", "boar", "macaque", "tiger", "bear", "crane", "penguin"]
poses = ["attack", "hit", "skill", "telegraph", "recover"]
base = "game/assets/sprites/player/poses"

count = 0

# 8 races
for r in races:
    r_dir = os.path.join(base, r)
    for p in poses:
        src = os.path.join(r_dir, f"{p}.png")
        if not os.path.exists(src):
            print(f"WARNING: src missing {src}")
            continue
        dst = os.path.join(r_dir, f"{p}_512.png")
        with Image.open(src) as img:
            img_rgba = img.convert("RGBA")
            # Strict LANCZOS resize to 512x512
            resized = img_rgba.resize((512, 512), resample=Image.Resampling.LANCZOS)
            resized.save(dst, format="PNG")
            count += 1
            print(f"Generated: {dst} (512x512, RGBA)")

# Rabbit (root poses and poses/rabbit)
rabbit_dir = os.path.join(base, "rabbit")
os.makedirs(rabbit_dir, exist_ok=True)

for p in poses:
    src = os.path.join(base, f"{p}.png")
    if not os.path.exists(src):
        print(f"WARNING: src missing {src}")
        continue
    dst_root = os.path.join(base, f"{p}_512.png")
    dst_rabbit = os.path.join(rabbit_dir, f"{p}_512.png")
    dst_rabbit_128 = os.path.join(rabbit_dir, f"{p}.png")

    with Image.open(src) as img:
        img_rgba = img.convert("RGBA")
        img_rgba.save(dst_rabbit_128, format="PNG")
        resized = img_rgba.resize((512, 512), resample=Image.Resampling.LANCZOS)
        resized.save(dst_root, format="PNG")
        resized.save(dst_rabbit, format="PNG")
        count += 1
        print(f"Generated: {dst_root} and {dst_rabbit} (512x512, RGBA)")

print(f"\nDone. Successfully processed all 9 races x 5 poses (total {count} pose sets).")
