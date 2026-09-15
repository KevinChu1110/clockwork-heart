import os
import re

workdir = "/opt/side/bravesoul-game"
paperdoll_dir = os.path.join(workdir, "game/assets/sprites/player/paperdoll")
godot_imported = os.path.join(workdir, "game/.godot/imported")

total = 0
missing_dest = []
missing_path = []
missing_ctex = []

for root, dirs, files in os.walk(paperdoll_dir):
    for f in files:
        if f.endswith(".import"):
            total += 1
            p = os.path.join(root, f)
            rel = os.path.relpath(p, workdir)
            with open(p, "r", encoding="utf-8") as fp:
                txt = fp.read()
            if "dest_files=" not in txt:
                missing_dest.append(rel)
            if "path=" not in txt:
                missing_path.append(rel)
            m = re.search(r'path="res://\.godot/imported/([^"]+)"', txt)
            if m:
                ctex = m.group(1)
                if not os.path.exists(os.path.join(godot_imported, ctex)):
                    missing_ctex.append((rel, ctex))

print(f"Total paperdoll .import files: {total}")
print(f"Missing dest_files: {len(missing_dest)}")
for p in missing_dest:
    print(" ", p)
print(f"Missing path: {len(missing_path)}")
for p in missing_path:
    print(" ", p)
print(f"Missing ctex file: {len(missing_ctex)}")
for rel, ctex in missing_ctex:
    print(" ", rel, "->", ctex)
