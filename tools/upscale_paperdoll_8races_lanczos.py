import os
from PIL import Image

races = ['fox', 'lion', 'boar', 'macaque', 'tiger', 'crane', 'bear', 'penguin']
base = 'game/assets/sprites/player/paperdoll'
slots = ['chassis', 'head_unit', 'optic_core']

processed = []

for r in races:
    for s in slots:
        slot_dir = os.path.join(base, r, s)
        if not os.path.exists(slot_dir):
            continue
        files = sorted([f for f in os.listdir(slot_dir) if f.endswith('.png') and not f.endswith('_512.png')])
        for f in files:
            src_path = os.path.join(slot_dir, f)
            name_no_ext, ext = os.path.splitext(f)
            dst_name = f"{name_no_ext}_512.png"
            dst_path = os.path.join(slot_dir, dst_name)

            with Image.open(src_path) as img:
                img_rgba = img.convert('RGBA')
                # Strict LANCZOS resize to 512x512
                resized = img_rgba.resize((512, 512), resample=Image.Resampling.LANCZOS)
                resized.save(dst_path, format='PNG')
                processed.append((r, s, dst_name, dst_path))

print(f"Successfully generated {len(processed)} 512x512 files using Image.Resampling.LANCZOS.")
