import os

races = ['fox', 'lion', 'boar', 'macaque', 'tiger', 'crane', 'bear', 'penguin']
base = 'game/assets/sprites/player/paperdoll'

for r in races:
    r_dir = os.path.join(base, r)
    if os.path.exists(r_dir):
        all_subdirs = sorted([d for d in os.listdir(r_dir) if os.path.isdir(os.path.join(r_dir, d))])
        print(f"=== {r} subdirs: {all_subdirs} ===")
        for d in all_subdirs:
            p = os.path.join(r_dir, d)
            files = sorted([f for f in os.listdir(p) if f.endswith('.png')])
            print(f"  {d}: {files}")
