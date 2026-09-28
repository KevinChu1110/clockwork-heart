import os, glob

builders = glob.glob("tools/build_*_combat_poses.py")
for b in sorted(builders):
    with open(b) as f:
        content = f.read()
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if "shift" in line.lower() and "body" in line.lower():
            print(f"{b}:{i+1}: {line}")
        elif "scale" in line.lower() and "body" in line.lower():
            print(f"{b}:{i+1}: {line}")
        elif "t>=" in line.lower() or "top >=" in line.lower():
            print(f"{b}:{i+1}: {line}")
