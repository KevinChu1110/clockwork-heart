import os

races = ['fox', 'lion', 'boar', 'macaque', 'tiger', 'crane', 'bear', 'penguin']
base = 'game/assets/sprites/player/paperdoll'
slots = ['chassis', 'head_unit', 'optic_core']

total_files = []
for r in races:
    for s in slots:
        p = os.path.join(base, r, s)
        if os.path.exists(p):
            files = sorted([f for f in os.listdir(p) if f.endswith('.png') and not f.endswith('_512.png')])
            for f in files:
                total_files.append((r, s, f, os.path.join(p, f)))

print(f"Total source files to upscale: {len(total_files)}")
for r, s, f, path in total_files:
    print(f"[{r}][{s}] {f} -> {f[:-4]}_512.png")
