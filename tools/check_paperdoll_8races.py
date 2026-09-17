import os
from PIL import Image

races = ['fox', 'lion', 'boar', 'macaque', 'tiger', 'crane', 'bear', 'penguin']
base = 'game/assets/sprites/player/paperdoll'

for r in races:
    r_dir = os.path.join(base, r)
    if os.path.exists(r_dir):
        print(f"=== {r} ===")
        for sd in ['chassis', 'head_unit', 'optic_core']:
            p = os.path.join(r_dir, sd)
            if os.path.exists(p):
                files = sorted([f for f in os.listdir(p) if f.endswith('.png')])
                for f in files:
                    fp = os.path.join(p, f)
                    with Image.open(fp) as img:
                        print(f"  {sd}/{f}: size={img.size}, mode={img.mode}")
            else:
                print(f"  {sd}: NOT FOUND")
    else:
        print(f"=== {r}: NOT FOUND ===")
